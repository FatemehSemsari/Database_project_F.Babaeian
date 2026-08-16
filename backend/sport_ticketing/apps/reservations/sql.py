GET_AVAILABLE_SEATS = """
SELECT
    si.invid AS inventory_id,
    s.seatid AS seat_id,

    s.rownumber AS row_number,
    s.seatnumber AS seat_number,

    vs.secid AS section_id,
    vs.secname AS section_name,

    tc.catid AS ticket_category_id,
    tc.catname AS ticket_category_name,
    tc.price AS price

FROM ticketcategory AS tc

INNER JOIN event AS e
    ON e.eid = tc.eid

INNER JOIN venuesection AS vs
    ON vs.secid = tc.secid

INNER JOIN seat AS s
    ON s.secid = vs.secid

INNER JOIN seatinventory AS si
    ON si.seatid = s.seatid
    AND si.eid = tc.eid
    AND si.catid = tc.catid

WHERE
    tc.catid = %s

    AND e.eventdate > NOW()

    AND LOWER(COALESCE(e.status, '')) = 'scheduled'

    AND (
        tc.startdate IS NULL
        OR tc.startdate <= NOW()
    )

    AND (
        tc.enddate IS NULL
        OR tc.enddate > NOW()
    )

    AND COALESCE(s.isactive, TRUE) = TRUE

    AND (
        LOWER(COALESCE(si.status, '')) = 'available'

        OR (
            LOWER(COALESCE(si.status, '')) = 'held'
            AND si.held_until IS NOT NULL
            AND si.held_until <= NOW()
        )
    )

ORDER BY
    s.rownumber ASC NULLS LAST,
    s.seatnumber ASC NULLS LAST;
"""


GET_INVENTORY_FOR_RESERVATION = """
SELECT
    si.invid AS inventory_id,
    si.seatid AS seat_id,
    si.status AS inventory_status,
    si.held_until AS held_until,

    s.rownumber AS row_number,
    s.seatnumber AS seat_number,
    s.isactive AS seat_is_active,

    tc.catid AS ticket_category_id,
    tc.catname AS ticket_category_name,
    tc.price AS price,
    tc.startdate AS sales_start_at,
    tc.enddate AS sales_end_at,

    e.eid AS event_id,
    e.eventdate AS event_datetime,
    e.status AS event_status,

    (
        LOWER(COALESCE(si.status, '')) = 'available'

        OR (
            LOWER(COALESCE(si.status, '')) = 'held'
            AND si.held_until IS NOT NULL
            AND si.held_until <= NOW()
        )
    ) AS inventory_available,

    (
        e.eventdate > NOW()

        AND LOWER(COALESCE(e.status, '')) = 'scheduled'

        AND (
            tc.startdate IS NULL
            OR tc.startdate <= NOW()
        )

        AND (
            tc.enddate IS NULL
            OR tc.enddate > NOW()
        )
    ) AS sale_open

FROM seatinventory AS si

INNER JOIN ticketcategory AS tc
    ON tc.catid = si.catid
    AND tc.eid = si.eid

INNER JOIN event AS e
    ON e.eid = si.eid

INNER JOIN seat AS s
    ON s.seatid = si.seatid
    AND s.secid = tc.secid

WHERE
    si.invid = %s
    AND tc.catid = %s

FOR UPDATE OF si;
"""


CREATE_RESERVATION = """
INSERT INTO reservation (
    user_id,
    event_id,
    status,
    reserved_at,
    total_amount,
    expires_at,
    paid_at
)
VALUES (
    %s,
    %s,
    'pending',
    NOW(),
    %s,
    %s,
    NULL
)
RETURNING
    reservation_id,
    event_id,
    status,
    reserved_at,
    total_amount,
    expires_at;
"""


CREATE_RESERVATION_ITEM = """
INSERT INTO reservation_item (
    reservation_id,
    cat_id,
    qty,
    price
)
VALUES (
    %s,
    %s,
    1,
    %s
)
RETURNING item_id;
"""

HOLD_INVENTORY = """
UPDATE seatinventory
SET
    status = 'held',
    reservation_id = %s,
    reservekey = %s,
    held_until = %s
WHERE invid = %s
RETURNING
    invid AS inventory_id,
    seatid AS seat_id,
    held_until;
"""

EXPIRE_PENDING_RESERVATIONS = """
UPDATE reservation
SET status = 'expired'
WHERE
    LOWER(COALESCE(status, '')) = 'pending'
    AND expires_at IS NOT NULL
    AND expires_at <= NOW();
"""


RELEASE_EXPIRED_INVENTORY = """
UPDATE seatinventory
SET
    status = 'available',
    reservation_id = NULL,
    reservekey = NULL,
    held_until = NULL
WHERE
    LOWER(COALESCE(status, '')) = 'held'
    AND held_until IS NOT NULL
    AND held_until <= NOW();
"""


GET_ACTIVE_USER_RESERVATIONS = """
SELECT
    r.reservation_id,
    r.event_id,

    e.eventdate AS event_datetime,

    home_team.tname AS home_team_name,
    away_team.tname AS away_team_name,

    v.name AS venue_name,
    c.name AS city_name,

    tc.catid AS ticket_category_id,
    tc.catname AS ticket_category_name,

    r.status,

    ri.qty AS quantity,
    ri.price AS price,

    r.total_amount,
    r.reserved_at,
    r.expires_at,
    r.paid_at,

    GREATEST(
        EXTRACT(
            EPOCH FROM (
                r.expires_at - NOW()
            )
        )::INTEGER,
        0
    ) AS remaining_seconds,

    seats.items AS seats

FROM reservation AS r

INNER JOIN event AS e
    ON e.eid = r.event_id

INNER JOIN teams AS home_team
    ON home_team.teamid = e.hometeam

INNER JOIN teams AS away_team
    ON away_team.teamid = e.awayteam

INNER JOIN venue AS v
    ON v.venueid = e.venueid

LEFT JOIN cities AS c
    ON c.cid = v.cityid

INNER JOIN reservation_item AS ri
    ON ri.reservation_id = r.reservation_id

INNER JOIN ticketcategory AS tc
    ON tc.catid = ri.cat_id

LEFT JOIN LATERAL (
    SELECT
        COALESCE(
            JSON_AGG(
                JSON_BUILD_OBJECT(
                    'inventory_id', si.invid,
                    'seat_id', s.seatid,
                    'row_number', s.rownumber,
                    'seat_number', s.seatnumber,
                    'section_id', vs.secid,
                    'section_name', vs.secname
                )
                ORDER BY
                    s.rownumber,
                    s.seatnumber
            )
            FILTER (
                WHERE si.invid IS NOT NULL
            ),
            '[]'::JSON
        ) AS items

    FROM reservation_seat AS rs

    INNER JOIN seatinventory AS si
        ON si.invid = rs.inventory_id

    INNER JOIN seat AS s
        ON s.seatid = si.seatid

    INNER JOIN venuesection AS vs
        ON vs.secid = s.secid

    WHERE
        rs.reservation_id = r.reservation_id
        AND si.catid = tc.catid

) AS seats
    ON TRUE

WHERE
    r.user_id = %s

    AND LOWER(
        COALESCE(r.status, '')
    ) = 'pending'

    AND r.expires_at IS NOT NULL

    AND r.expires_at > NOW()

ORDER BY
    r.expires_at ASC;
"""


GET_USER_RESERVATION_HISTORY = """
SELECT
    r.reservation_id,
    r.event_id,

    e.eventdate AS event_datetime,

    home_team.tname AS home_team_name,
    away_team.tname AS away_team_name,

    v.name AS venue_name,
    c.name AS city_name,

    tc.catid AS ticket_category_id,
    tc.catname AS ticket_category_name,

    r.status,

    ri.qty AS quantity,
    ri.price AS price,

    r.total_amount,
    r.reserved_at,
    r.expires_at,
    r.paid_at,

    NULL::INTEGER AS remaining_seconds,

    seats.items AS seats

FROM reservation AS r

INNER JOIN event AS e
    ON e.eid = r.event_id

INNER JOIN teams AS home_team
    ON home_team.teamid = e.hometeam

INNER JOIN teams AS away_team
    ON away_team.teamid = e.awayteam

INNER JOIN venue AS v
    ON v.venueid = e.venueid

LEFT JOIN cities AS c
    ON c.cid = v.cityid

INNER JOIN reservation_item AS ri
    ON ri.reservation_id = r.reservation_id

INNER JOIN ticketcategory AS tc
    ON tc.catid = ri.cat_id

LEFT JOIN LATERAL (
    SELECT
        COALESCE(
            JSON_AGG(
                JSON_BUILD_OBJECT(
                    'inventory_id', si.invid,
                    'seat_id', s.seatid,
                    'row_number', s.rownumber,
                    'seat_number', s.seatnumber,
                    'section_id', vs.secid,
                    'section_name', vs.secname
                )
                ORDER BY
                    s.rownumber,
                    s.seatnumber
            )
            FILTER (
                WHERE si.invid IS NOT NULL
            ),
            '[]'::JSON
        ) AS items

    FROM reservation_seat AS rs

    INNER JOIN seatinventory AS si
        ON si.invid = rs.inventory_id

    INNER JOIN seat AS s
        ON s.seatid = si.seatid

    INNER JOIN venuesection AS vs
        ON vs.secid = s.secid

    WHERE
        rs.reservation_id = r.reservation_id
        AND si.catid = tc.catid

) AS seats
    ON TRUE

WHERE
    r.user_id = %s

    AND LOWER(
        COALESCE(r.status, '')
    ) IN (
        'paid',
        'expired',
        'cancelled'
    )

ORDER BY
    r.reserved_at DESC;
"""


CREATE_RESERVATION_SEAT = """
INSERT INTO reservation_seat (
    reservation_id,
    inventory_id
)
VALUES (
    %s,
    %s
)
RETURNING reservation_id, inventory_id;
"""
