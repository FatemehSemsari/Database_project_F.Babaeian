CHECK_USER_EXISTS_BY_EMAIL_OR_PHONE = """
SELECT id
FROM users
WHERE
    (%s IS NOT NULL AND email = %s)
    OR
    (%s IS NOT NULL AND phone = %s)
LIMIT 1;
"""


CREATE_USER = """
INSERT INTO users (
    first_name,
    last_name,
    email,
    phone,
    password_hash,
    role,
    email_verified,
    phone_verified,
    is_active,
    created_at,
    updated_at
)
VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, TRUE, NOW(), NOW()
)
RETURNING
    id,
    first_name,
    last_name,
    email,
    phone,
    role,
    email_verified,
    phone_verified,
    is_active,
    created_at;
"""

GET_USER_BY_ID = """
SELECT
    id,
    first_name,
    last_name,
    email,
    phone,
    role,
    email_verified,
    phone_verified,
    is_active,
    created_at,
    updated_at
FROM users
WHERE id = %s
LIMIT 1;
"""

GET_USER_BY_EMAIL = """
SELECT
    id,
    first_name,
    last_name,
    email,
    phone,
    email_verified,
    phone_verified,
    password_hash,
    role,
    is_active,
    created_at
FROM users
WHERE email = %s
LIMIT 1;
"""

GET_USER_BY_PHONE = """
SELECT
    id,
    first_name,
    last_name,
    email,
    phone,
    role,
    email_verified,
    phone_verified,
    password_hash,
    is_active,
    created_at
FROM users
WHERE phone = %s
LIMIT 1;
"""

# COALESCE -> If firstname or lastname was equal to None, the previous value will not be corrupted.

UPDATE_USER_PROFILE = """
UPDATE users
SET
    first_name = COALESCE(%s, first_name),
    last_name = COALESCE(%s, last_name),
    updated_at = NOW()
WHERE id = %s
  AND is_active = TRUE
RETURNING
    id,
    first_name,
    last_name,
    email,
    phone,
    role,
    email_verified,
    phone_verified,
    is_active,
    created_at,
    updated_at;
"""

#return password_hash to be checked with user's password
GET_USER_AUTH_BY_ID = """
SELECT
    id,
    first_name,
    last_name,
    email,
    phone,
    password_hash,
    role,
    email_verified,
    phone_verified,
    is_active,
    created_at,
    updated_at
FROM users
WHERE id = %s
LIMIT 1;
"""


UPDATE_USER_EMAIL = """
UPDATE users
SET
    email = %s,
    email_verified = TRUE,
    updated_at = NOW()
WHERE id = %s
  AND is_active = TRUE
RETURNING
    id,
    first_name,
    last_name,
    email,
    phone,
    role,
    email_verified,
    phone_verified,
    is_active,
    created_at,
    updated_at;
"""


UPDATE_USER_PHONE = """
UPDATE users
SET
    phone = %s,
    phone_verified = TRUE,
    updated_at = NOW()
WHERE id = %s
  AND is_active = TRUE
RETURNING
    id,
    first_name,
    last_name,
    email,
    phone,
    role,
    email_verified,
    phone_verified,
    is_active,
    created_at,
    updated_at;
"""

UPDATE_USER_PASSWORD = """
UPDATE users
SET
    password_hash = %s,
    updated_at = NOW()
WHERE id = %s
  AND is_active = TRUE
RETURNING id;
"""
LIST_CITIES = """
SELECT
    c.cid AS id,
    c.name AS name,

    p.province_id AS province_id,
    p.name AS province_name,

    co.country_id AS country_id,
    co.name AS country_name,
    co.iso_code AS country_iso_code

FROM cities AS c

LEFT JOIN provinces AS p
    ON p.province_id = c.province_id

LEFT JOIN countries AS co
    ON co.country_id = p.country_id

WHERE
    (
        %s IS NULL
        OR c.province_id = %s
    )
    AND
    (
        %s IS NULL
        OR p.country_id = %s
    )
    AND
    (
        %s IS NULL
        OR c.name ILIKE %s
    )

ORDER BY
    co.name ASC NULLS LAST,
    p.name ASC NULLS LAST,
    c.name ASC;
"""




LIST_VENUES = """
SELECT
    v.venueid AS id,
    v.name AS name,
    v.address AS address,
    v.capacity AS capacity,

    c.cid AS city_id,
    c.name AS city_name,

    p.province_id AS province_id,
    p.name AS province_name,

    co.country_id AS country_id,
    co.name AS country_name,
    co.iso_code AS country_iso_code

FROM venue AS v

LEFT JOIN cities AS c
    ON c.cid = v.cityid

LEFT JOIN provinces AS p
    ON p.province_id = c.province_id

LEFT JOIN countries AS co
    ON co.country_id = p.country_id

WHERE
    (
        %s IS NULL
        OR v.cityid = %s
    )
    AND
    (
        %s IS NULL
        OR c.province_id = %s
    )
    AND
    (
        %s IS NULL
        OR p.country_id = %s
    )
    AND
    (
        %s IS NULL
        OR v.name ILIKE %s
        OR COALESCE(v.address, '') ILIKE %s
    )

ORDER BY
    co.name ASC NULLS LAST,
    p.name ASC NULLS LAST,
    c.name ASC NULLS LAST,
    v.name ASC;
"""




LIST_SPORTS = """
SELECT
    s.sid AS id,
    s.sname AS name

FROM sports AS s

WHERE
    (
        %s IS NULL
        OR s.sname ILIKE %s
    )

ORDER BY
    s.sname ASC;
"""




LIST_LEAGUES = """
SELECT
    l.lid AS id,
    l.lname AS name,
    l.season AS season,
    l.start_date AS start_date,
    l.end_date AS end_date,

    s.sid AS sport_id,
    s.sname AS sport_name

FROM league AS l

LEFT JOIN sports AS s
    ON s.sid = l.sportid

WHERE
    (
        %s IS NULL
        OR l.sportid = %s
    )
    AND
    (
        %s IS NULL
        OR l.season = %s
    )
    AND
    (
        %s IS NULL
        OR l.lname ILIKE %s
    )

ORDER BY
    s.sname ASC NULLS LAST,
    l.lname ASC,
    l.start_date DESC NULLS LAST;
"""



LIST_TEAMS = """
SELECT
    t.teamid AS id,
    t.tname AS name,
    t.logo_url AS logo_url,

    s.sid AS sport_id,
    s.sname AS sport_name,

    c.cid AS city_id,
    c.name AS city_name,

    p.province_id AS province_id,
    p.name AS province_name,

    co.country_id AS country_id,
    co.name AS country_name,
    co.iso_code AS country_iso_code

FROM teams AS t

LEFT JOIN sports AS s
    ON s.sid = t.sportid

LEFT JOIN cities AS c
    ON c.cid = t.city_id

LEFT JOIN provinces AS p
    ON p.province_id = c.province_id

LEFT JOIN countries AS co
    ON co.country_id = p.country_id

WHERE
    (
        %s IS NULL
        OR t.city_id = %s
    )
    AND
    (
        %s IS NULL
        OR t.sportid = %s
    )
    AND
    (
        %s IS NULL
        OR EXISTS (
            SELECT 1
            FROM league_team AS lt
            WHERE
                lt.team_id = t.teamid
                AND lt.league_id = %s
        )
    )
    AND
    (
        %s IS NULL
        OR t.tname ILIKE %s
    )

ORDER BY
    co.name ASC NULLS LAST,
    p.name ASC NULLS LAST,
    c.name ASC NULLS LAST,
    t.tname ASC;
"""
GET_USER_TICKET_REPORT_TARGET = """
SELECT
    t.tid AS ticket_id,
    t.reservation_id,
    t.status AS ticket_status,

    r.user_id,
    r.event_id,
    r.status AS reservation_status

FROM ticket AS t

INNER JOIN reservation AS r
    ON r.reservation_id = t.reservation_id

WHERE
    t.tid = %s
    AND r.user_id = %s

LIMIT 1;
"""



GET_USER_RESERVATION_REPORT_TARGET = """
SELECT
    r.reservation_id,
    r.user_id,
    r.event_id,
    r.status AS reservation_status

FROM reservation AS r

WHERE
    r.reservation_id = %s
    AND r.user_id = %s

LIMIT 1;
"""



CREATE_REPORT = """
INSERT INTO report (
    user_id,
    tid,
    reservation_id,
    subject,
    message,
    status
)
VALUES (
    %s,
    %s,
    %s,
    %s,
    %s,
    'pending'
)
RETURNING
    reportid AS report_id,
    user_id,
    tid AS ticket_id,
    reservation_id,
    subject AS issue_type,
    message,
    status;
"""


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
LIST_CANCELLED_TICKETS = """
SELECT
    t.tid AS ticket_id,
    t.serialnum AS serial_number,
    t.status AS ticket_status,
    t.issuedate AS issued_at,

    r.reservation_id,
    r.status AS reservation_status,

    u.id AS user_id,
    u.first_name,
    u.last_name,
    u.email,
    u.phone,

    e.eid AS event_id,
    e.eventdate AS event_datetime,

    home_team.tname AS home_team_name,
    away_team.tname AS away_team_name,

    v.name AS venue_name,

    si.invid AS inventory_id,

    s.rownumber AS row_number,
    s.seatnumber AS seat_number,

    vs.secname AS section_name

FROM ticket AS t

INNER JOIN reservation AS r
    ON r.reservation_id = t.reservation_id

INNER JOIN users AS u
    ON u.id = r.user_id

INNER JOIN event AS e
    ON e.eid = r.event_id

INNER JOIN teams AS home_team
    ON home_team.teamid = e.hometeam

INNER JOIN teams AS away_team
    ON away_team.teamid = e.awayteam

INNER JOIN venue AS v
    ON v.venueid = e.venueid

INNER JOIN seatinventory AS si
    ON si.invid = t.invid

INNER JOIN seat AS s
    ON s.seatid = si.seatid

INNER JOIN venuesection AS vs
    ON vs.secid = s.secid

WHERE
    LOWER(COALESCE(t.status, ''))
        = 'cancelled'

ORDER BY
    t.tid DESC

LIMIT %s
OFFSET %s;
"""

LIST_SUSPICIOUS_PAYMENTS = """
SELECT
    p.id AS payment_id,
    p.reservation_id,

    p.amount,
    p.method,
    p.status AS payment_status,

    p.created_at,
    p.paid_at,

    p.refund_amount,
    p.refunded_at,

    p.transaction_ref,

    r.total_amount AS reservation_amount,
    r.status AS reservation_status,

    u.id AS user_id,
    u.first_name,
    u.last_name,
    u.email,
    u.phone,

    suspicion.suspicion_reasons

FROM payment AS p

INNER JOIN reservation AS r
    ON r.reservation_id = p.reservation_id

INNER JOIN users AS u
    ON u.id = r.user_id

CROSS JOIN LATERAL (
    SELECT
        ARRAY_REMOVE(
            ARRAY[

                CASE
                    WHEN p.amount
                         <> r.total_amount
                    THEN 'amount_mismatch'
                END,

                CASE
                    WHEN
                        LOWER(
                            COALESCE(
                                p.status,
                                ''
                            )
                        ) = 'successful'
                        AND p.paid_at IS NULL
                    THEN
                        'successful_without_paid_at'
                END,

                CASE
                    WHEN
                        LOWER(
                            COALESCE(
                                p.status,
                                ''
                            )
                        ) = 'successful'

                        AND LOWER(
                            COALESCE(
                                r.status,
                                ''
                            )
                        ) <> 'paid'

                    THEN
                        'successful_payment_but_reservation_not_paid'
                END,

                CASE
                    WHEN
                        LOWER(
                            COALESCE(
                                p.status,
                                ''
                            )
                        ) = 'refunded'

                        AND p.refund_amount IS NULL

                    THEN
                        'refunded_without_refund_amount'
                END,

                CASE
                    WHEN
                        p.refund_amount IS NOT NULL

                        AND p.refund_amount
                            > p.amount

                    THEN
                        'refund_exceeds_payment'
                END,

                CASE
                    WHEN
                        p.refunded_at IS NOT NULL

                        AND LOWER(
                            COALESCE(
                                p.status,
                                ''
                            )
                        ) <> 'refunded'

                    THEN
                        'refund_status_mismatch'
                END,

                CASE
                    WHEN (
                        SELECT COUNT(*)

                        FROM payment AS p2

                        WHERE
                            p2.reservation_id
                                = p.reservation_id

                            AND LOWER(
                                COALESCE(
                                    p2.status,
                                    ''
                                )
                            ) = 'successful'
                    ) > 1

                    THEN
                        'multiple_successful_payments'
                END

            ],
            NULL
        ) AS suspicion_reasons

) AS suspicion

WHERE
    CARDINALITY(
        suspicion.suspicion_reasons
    ) > 0

ORDER BY
    p.created_at DESC

LIMIT %s
OFFSET %s;
"""


LIST_SUPPORT_REPORTS = """
SELECT
    rp.reportid AS report_id,

    rp.user_id,

    u.first_name,
    u.last_name,
    u.email,
    u.phone,

    rp.tid AS ticket_id,
    rp.reservation_id,

    rp.subject AS issue_type,
    rp.message,

    rp.status,

    rp.support_response,

    rp.reviewed_by,
    rp.reviewed_at,

    reviewer.first_name
        AS reviewer_first_name,

    reviewer.last_name
        AS reviewer_last_name

FROM report AS rp

INNER JOIN users AS u
    ON u.id = rp.user_id

LEFT JOIN users AS reviewer
    ON reviewer.id = rp.reviewed_by

WHERE
    (
        %s IS NULL
        OR LOWER(rp.status) = LOWER(%s)
    )

    AND (
        %s IS NULL
        OR LOWER(rp.subject) = LOWER(%s)
    )

ORDER BY
    rp.reportid DESC

LIMIT %s
OFFSET %s;
"""


UPDATE_SUPPORT_REPORT = """
UPDATE report

SET
    status = COALESCE(
        %s,
        status
    ),

    support_response = COALESCE(
        %s,
        support_response
    ),

    reviewed_by = %s,

    reviewed_at = NOW()

WHERE reportid = %s

RETURNING
    reportid AS report_id,
    user_id,
    tid AS ticket_id,
    reservation_id,
    subject AS issue_type,
    message,
    status,
    support_response,
    reviewed_by,
    reviewed_at;
"""


LIST_SUPPORT_RESERVATIONS = """
SELECT
    r.reservation_id,

    r.user_id,

    u.first_name,
    u.last_name,
    u.email,
    u.phone,

    r.event_id,

    e.eventdate AS event_datetime,

    home_team.tname AS home_team_name,
    away_team.tname AS away_team_name,

    r.status AS reservation_status,

    r.support_review_status,

    r.support_note,

    r.reserved_at,
    r.expires_at,
    r.paid_at,

    r.total_amount,

    r.support_reviewed_by,
    r.support_reviewed_at,

    seat_info.inventory_id,
    seat_info.row_number,
    seat_info.seat_number,
    seat_info.section_name,

    ticket_info.ticket_id,
    ticket_info.ticket_status

FROM reservation AS r

INNER JOIN users AS u
    ON u.id = r.user_id

INNER JOIN event AS e
    ON e.eid = r.event_id

INNER JOIN teams AS home_team
    ON home_team.teamid = e.hometeam

INNER JOIN teams AS away_team
    ON away_team.teamid = e.awayteam

LEFT JOIN LATERAL (
    SELECT
        si.invid AS inventory_id,

        s.rownumber AS row_number,
        s.seatnumber AS seat_number,

        vs.secname AS section_name

    FROM reservation_seat AS rs

    INNER JOIN seatinventory AS si
        ON si.invid = rs.inventory_id

    INNER JOIN seat AS s
        ON s.seatid = si.seatid

    INNER JOIN venuesection AS vs
        ON vs.secid = s.secid

    WHERE
        rs.reservation_id
            = r.reservation_id

    LIMIT 1

) AS seat_info
    ON TRUE

LEFT JOIN LATERAL (
    SELECT
        t.tid AS ticket_id,
        t.status AS ticket_status

    FROM ticket AS t

    WHERE
        t.reservation_id
            = r.reservation_id

    ORDER BY t.tid DESC

    LIMIT 1

) AS ticket_info
    ON TRUE

WHERE
    (
        %s IS NULL

        OR LOWER(
            COALESCE(
                r.status,
                ''
            )
        ) = LOWER(%s)
    )

    AND (
        %s IS NULL

        OR LOWER(
            r.support_review_status
        ) = LOWER(%s)
    )

ORDER BY
    r.reserved_at DESC

LIMIT %s
OFFSET %s;
"""


GET_RESERVATION_FOR_SUPPORT_UPDATE = """
SELECT
    r.reservation_id,
    r.user_id,
    r.event_id,

    r.status AS reservation_status,

    r.support_review_status,

    r.reserved_at,
    r.expires_at,
    r.paid_at,

    r.total_amount

FROM reservation AS r

WHERE
    r.reservation_id = %s

FOR UPDATE;
"""


APPROVE_RESERVATION_BY_SUPPORT = """
UPDATE reservation

SET
    support_review_status = 'approved',

    support_reviewed_by = %s,

    support_reviewed_at = NOW(),

    support_note = %s

WHERE
    reservation_id = %s

RETURNING
    reservation_id,

    status AS reservation_status,

    support_review_status,

    support_note,

    support_reviewed_by,

    support_reviewed_at;
"""

MODIFY_RESERVATION_EXPIRY = """
UPDATE reservation

SET
    expires_at = %s,

    support_review_status = 'modified',

    support_reviewed_by = %s,

    support_reviewed_at = NOW(),

    support_note = %s

WHERE
    reservation_id = %s

RETURNING
    reservation_id,

    status AS reservation_status,

    expires_at,

    support_review_status,

    support_note,

    support_reviewed_by,

    support_reviewed_at;
"""


SYNC_RESERVATION_INVENTORY_EXPIRY = """
UPDATE seatinventory AS si

SET
    held_until = %s

FROM reservation_seat AS rs

WHERE
    rs.reservation_id = %s

    AND rs.inventory_id = si.invid

    AND LOWER(
        COALESCE(
            si.status,
            ''
        )
    ) = 'held'

    AND si.reservation_id = %s;
"""


CANCEL_RESERVATION_BY_SUPPORT = """
UPDATE reservation

SET
    status = 'cancelled',

    support_review_status = 'cancelled',

    support_reviewed_by = %s,

    support_reviewed_at = NOW(),

    support_note = %s

WHERE
    reservation_id = %s

RETURNING
    reservation_id,

    status AS reservation_status,

    support_review_status,

    support_note,

    support_reviewed_by,

    support_reviewed_at;
"""



RELEASE_SUPPORT_CANCELLED_RESERVATION = """
UPDATE seatinventory AS si

SET
    status = 'available',

    reservation_id = NULL,

    reservekey = NULL,

    held_until = NULL

FROM reservation_seat AS rs

WHERE
    rs.reservation_id = %s

    AND rs.inventory_id = si.invid

    AND si.reservation_id = %s

    AND LOWER(
        COALESCE(
            si.status,
            ''
        )
    ) = 'held';
"""


SEARCH_TICKETS_BASE = """
SELECT
    e.eid AS event_id,
    e.eventdate AS event_datetime,
    e.status AS event_status,

    s.sid AS sport_id,
    s.sname AS sport_name,

    l.lid AS league_id,
    l.lname AS league_name,
    l.season AS league_season,

    v.venueid AS venue_id,
    v.name AS venue_name,
    v.address AS venue_address,
    v.capacity AS venue_capacity,

    c.cid AS city_id,
    c.name AS city_name,

    p.province_id AS province_id,
    p.name AS province_name,

    co.country_id AS country_id,
    co.name AS country_name,
    co.iso_code AS country_iso_code,

    home_team.teamid AS home_team_id,
    home_team.tname AS home_team_name,
    home_team.logo_url AS home_team_logo_url,

    away_team.teamid AS away_team_id,
    away_team.tname AS away_team_name,
    away_team.logo_url AS away_team_logo_url,

    tc.catid AS ticket_category_id,
    tc.catname AS ticket_category_name,
    tc.price AS current_price,
    tc.startdate AS sales_start_at,
    tc.enddate AS sales_end_at,

    vs.secid AS section_id,
    vs.secname AS section_name,
    vs.capacity AS section_capacity,

    st.stypeid AS section_type_id,
    st.typename AS section_type_name,

    availability.available_count AS available_count

FROM event AS e

INNER JOIN sports AS s
    ON s.sid = e.sportid

LEFT JOIN league AS l
    ON l.lid = e.leagueid

INNER JOIN venue AS v
    ON v.venueid = e.venueid

LEFT JOIN cities AS c
    ON c.cid = v.cityid

LEFT JOIN provinces AS p
    ON p.province_id = c.province_id

LEFT JOIN countries AS co
    ON co.country_id = p.country_id

INNER JOIN teams AS home_team
    ON home_team.teamid = e.hometeam

INNER JOIN teams AS away_team
    ON away_team.teamid = e.awayteam

INNER JOIN ticketcategory AS tc
    ON tc.eid = e.eid

INNER JOIN venuesection AS vs
    ON vs.secid = tc.secid

LEFT JOIN sectiontype AS st
    ON st.stypeid = vs.stypeid

LEFT JOIN LATERAL (
    SELECT
        COUNT(*)::INTEGER AS available_count

    FROM seatinventory AS si

    INNER JOIN seat AS seat_row
        ON seat_row.seatid = si.seatid

    WHERE
        si.eid = e.eid

        AND si.catid = tc.catid

        AND COALESCE(
            seat_row.isactive,
            TRUE
        ) = TRUE

        AND (
            LOWER(COALESCE(si.status, '')) = 'available'

            OR (
                LOWER(COALESCE(si.status, '')) = 'held'

                AND si.held_until IS NOT NULL

                AND si.held_until <= NOW()
            )
        )
) AS availability
    ON TRUE

WHERE
    e.eventdate >= NOW()

    AND LOWER(COALESCE(e.status, '')) = 'scheduled'

    AND (
        tc.startdate IS NULL
        OR NOW() >= tc.startdate
    )

    AND (
        tc.enddate IS NULL
        OR NOW() < tc.enddate
    )

    AND availability.available_count > 0
"""



SEARCH_TICKETS_ORDER_AND_PAGINATION = """
ORDER BY
    e.eventdate ASC,
    tc.price ASC,
    tc.catname ASC

LIMIT %s
OFFSET %s;
"""



GET_TICKET_DETAILS = """
SELECT
    e.eid AS event_id,
    e.eventdate AS event_datetime,
    e.status AS event_status,
    e.notes AS event_notes,
    e.homescore AS home_score,
    e.awayscore AS away_score,

    s.sid AS sport_id,
    s.sname AS sport_name,

    l.lid AS league_id,
    l.lname AS league_name,
    l.season AS league_season,
    l.start_date AS league_start_date,
    l.end_date AS league_end_date,

    v.venueid AS venue_id,
    v.name AS venue_name,
    v.address AS venue_address,
    v.capacity AS venue_capacity,

    c.cid AS city_id,
    c.name AS city_name,

    p.province_id AS province_id,
    p.name AS province_name,

    co.country_id AS country_id,
    co.name AS country_name,
    co.iso_code AS country_iso_code,

    home_team.teamid AS home_team_id,
    home_team.tname AS home_team_name,
    home_team.logo_url AS home_team_logo_url,

    away_team.teamid AS away_team_id,
    away_team.tname AS away_team_name,
    away_team.logo_url AS away_team_logo_url,

    tc.catid AS ticket_category_id,
    tc.catname AS ticket_category_name,
    tc.price AS current_price,
    tc.startdate AS sales_start_at,
    tc.enddate AS sales_end_at,

    vs.secid AS section_id,
    vs.secname AS section_name,
    vs.capacity AS section_capacity,

    st.stypeid AS section_type_id,
    st.typename AS section_type_name,

    availability.available_count AS available_count,

    current_policy.cancel_until AS cancel_until,
    current_policy.refund_percent AS refund_percent,
    current_policy.policy_notes AS policy_notes,

    (
        e.eventdate > NOW()

        AND LOWER(
            COALESCE(e.status, '')
        ) = 'scheduled'

        AND (
            tc.startdate IS NULL
            OR NOW() >= tc.startdate
        )

        AND (
            tc.enddate IS NULL
            OR NOW() < tc.enddate
        )
    ) AS is_sale_open,

    (
        e.eventdate > NOW()

        AND LOWER(
            COALESCE(e.status, '')
        ) = 'scheduled'

        AND (
            tc.startdate IS NULL
            OR NOW() >= tc.startdate
        )

        AND (
            tc.enddate IS NULL
            OR NOW() < tc.enddate
        )

        AND availability.available_count > 0
    ) AS is_available,

    amenities.items AS amenities

FROM ticketcategory AS tc

INNER JOIN event AS e
    ON e.eid = tc.eid

INNER JOIN sports AS s
    ON s.sid = e.sportid

LEFT JOIN league AS l
    ON l.lid = e.leagueid

INNER JOIN venue AS v
    ON v.venueid = e.venueid

LEFT JOIN cities AS c
    ON c.cid = v.cityid

LEFT JOIN provinces AS p
    ON p.province_id = c.province_id

LEFT JOIN countries AS co
    ON co.country_id = p.country_id

INNER JOIN teams AS home_team
    ON home_team.teamid = e.hometeam

INNER JOIN teams AS away_team
    ON away_team.teamid = e.awayteam

INNER JOIN venuesection AS vs
    ON vs.secid = tc.secid

LEFT JOIN sectiontype AS st
    ON st.stypeid = vs.stypeid

LEFT JOIN LATERAL (
    SELECT
        COUNT(*)::INTEGER AS available_count

    FROM seatinventory AS si

    INNER JOIN seat AS seat_row
        ON seat_row.seatid = si.seatid

    WHERE
        si.eid = e.eid

        AND si.catid = tc.catid

        AND COALESCE(
            seat_row.isactive,
            TRUE
        ) = TRUE

        AND (
            LOWER(COALESCE(si.status, '')) = 'available'

            OR (
                LOWER(COALESCE(si.status, '')) = 'held'

                AND si.held_until IS NOT NULL

                AND si.held_until <= NOW()
            )
        )
) AS availability
    ON TRUE

LEFT JOIN LATERAL (
    SELECT
        po.canceluntil AS cancel_until,
        po.refundpercent AS refund_percent,
        po.notes AS policy_notes

    FROM policy AS po

    WHERE
        po.eid = e.eid

    ORDER BY
        po.pid DESC

    LIMIT 1
) AS current_policy
    ON TRUE

LEFT JOIN LATERAL (
    SELECT
        COALESCE(
            JSON_AGG(
                JSON_BUILD_OBJECT(
                    'id', a.id,
                    'name', a.name
                )
                ORDER BY a.name
            )
            FILTER (
                WHERE a.id IS NOT NULL
            ),
            '[]'::JSON
        ) AS items

    FROM section_amenity AS sa

    INNER JOIN amenity AS a
        ON a.id = sa.amenity_id

    WHERE
        sa.section_id = vs.secid
) AS amenities
    ON TRUE

WHERE
    tc.catid = %s

LIMIT 1;
"""


GET_USER_BOOKINGS = """
SELECT
    t.tid AS ticket_id,
    t.serialnum AS serial_number,
    t.status AS ticket_status,
    t.issuedate AS issue_date,

    r.reservation_id,
    r.status AS reservation_status,
    r.total_amount,
    r.paid_at,

    e.eid AS event_id,
    e.eventdate AS event_datetime,

    s.sid AS sport_id,
    s.sname AS sport_name,

    l.lid AS league_id,
    l.lname AS league_name,
    l.season AS league_season,

    home_team.teamid AS home_team_id,
    home_team.tname AS home_team_name,
    home_team.logo_url AS home_team_logo_url,

    away_team.teamid AS away_team_id,
    away_team.tname AS away_team_name,
    away_team.logo_url AS away_team_logo_url,

    v.venueid AS venue_id,
    v.name AS venue_name,
    v.address AS venue_address,

    c.cid AS city_id,
    c.name AS city_name,

    tc.catid AS ticket_category_id,
    tc.catname AS ticket_category_name,

    purchase.purchase_price,

    vs.secid AS section_id,
    vs.secname AS section_name,

    seat_row.seatid AS seat_id,
    seat_row.rownumber AS row_number,
    seat_row.seatnumber AS seat_number,

    checkin.checked_in_at,
    checkin.gate,

    CASE
        WHEN
            LOWER(COALESCE(t.status, '')) = 'cancelled'
            OR LOWER(COALESCE(r.status, '')) = 'cancelled'
        THEN 'cancelled'

        WHEN checkin.checked_in_at IS NOT NULL
        THEN 'used'

        WHEN
            LOWER(COALESCE(t.status, '')) = 'valid'
            AND e.eventdate > NOW()
        THEN 'upcoming'

        ELSE 'past'
    END AS booking_state

FROM ticket AS t

INNER JOIN reservation AS r
    ON r.reservation_id = t.reservation_id

INNER JOIN event AS e
    ON e.eid = r.event_id

INNER JOIN sports AS s
    ON s.sid = e.sportid

LEFT JOIN league AS l
    ON l.lid = e.leagueid

INNER JOIN teams AS home_team
    ON home_team.teamid = e.hometeam

INNER JOIN teams AS away_team
    ON away_team.teamid = e.awayteam

INNER JOIN venue AS v
    ON v.venueid = e.venueid

LEFT JOIN cities AS c
    ON c.cid = v.cityid

INNER JOIN seatinventory AS si
    ON si.invid = t.invid

INNER JOIN ticketcategory AS tc
    ON tc.catid = si.catid

INNER JOIN seat AS seat_row
    ON seat_row.seatid = si.seatid

INNER JOIN venuesection AS vs
    ON vs.secid = seat_row.secid

LEFT JOIN LATERAL (
    SELECT
        ri.price AS purchase_price

    FROM reservation_item AS ri

    WHERE
        ri.reservation_id = r.reservation_id
        AND ri.cat_id = si.catid

    ORDER BY
        ri.item_id ASC

    LIMIT 1
) AS purchase
    ON TRUE

LEFT JOIN LATERAL (
    SELECT
        cl.entertime AS checked_in_at,
        cl.gate AS gate

    FROM checkinlog AS cl

    WHERE cl.tid = t.tid

    ORDER BY
        cl.logid DESC

    LIMIT 1
) AS checkin
    ON TRUE

WHERE
    r.user_id = %s

ORDER BY
    e.eventdate DESC,
    t.tid DESC;
"""


GET_TICKET_CANCELLATION_INFO = """
SELECT
    t.tid AS ticket_id,
    t.status AS ticket_status,

    r.reservation_id,
    r.status AS reservation_status,

    e.eid AS event_id,
    e.eventdate AS event_datetime,

    o.organizer_id,
    o.name AS organizer_name,

    tc.catid AS ticket_category_id,
    tc.catname AS ticket_category_name,

    purchase.purchase_price,

    GREATEST(
        time_info.remaining_hours,
        0
    ) AS remaining_hours,

    selected_rule.rule_id,

    selected_rule.min_hours_before_event,
    selected_rule.max_hours_before_event,

    selected_rule.refund_percent,

    selected_rule.rule_can_cancel,

    selected_rule.rule_notes,

    EXISTS (
        SELECT 1
        FROM checkinlog AS cl
        WHERE cl.tid = t.tid
    ) AS is_used,

    (
        e.eventdate <= NOW()
    ) AS event_started

FROM ticket AS t

INNER JOIN reservation AS r
    ON r.reservation_id = t.reservation_id

INNER JOIN event AS e
    ON e.eid = r.event_id

INNER JOIN organizer AS o
    ON o.organizer_id = e.organizer_id

INNER JOIN seatinventory AS si
    ON si.invid = t.invid

INNER JOIN ticketcategory AS tc
    ON tc.catid = si.catid

LEFT JOIN LATERAL (
    SELECT
        ri.price AS purchase_price

    FROM reservation_item AS ri

    WHERE
        ri.reservation_id = r.reservation_id
        AND ri.cat_id = tc.catid

    ORDER BY
        ri.item_id ASC

    LIMIT 1
) AS purchase
    ON TRUE

CROSS JOIN LATERAL (
    SELECT
        EXTRACT(
            EPOCH FROM (
                e.eventdate - NOW()
            )
        ) / 3600.0 AS remaining_hours
) AS time_info

LEFT JOIN LATERAL (
    SELECT
        cr.rule_id,

        cr.min_hours_before_event,
        cr.max_hours_before_event,

        cr.refund_percent,

        cr.can_cancel AS rule_can_cancel,

        cr.notes AS rule_notes

    FROM cancellation_rule AS cr

    WHERE
        cr.organizer_id = e.organizer_id

        AND cr.is_active = TRUE

        AND time_info.remaining_hours
            >= cr.min_hours_before_event

        AND (
            cr.max_hours_before_event IS NULL

            OR time_info.remaining_hours
               < cr.max_hours_before_event
        )

    ORDER BY
        cr.min_hours_before_event DESC

    LIMIT 1
) AS selected_rule
    ON TRUE

WHERE
    t.tid = %s
    AND r.user_id = %s

LIMIT 1;
"""


GET_TICKET_FOR_CANCELLATION = """
SELECT
    t.tid AS ticket_id,
    t.status AS ticket_status,
    t.invid AS inventory_id,

    r.reservation_id,
    r.user_id,
    r.status AS reservation_status,

    e.eid AS event_id,
    e.eventdate AS event_datetime,
    e.organizer_id,

    (
        e.eventdate <= NOW()
    ) AS event_started,

    si.catid AS ticket_category_id,
    si.status AS inventory_status,

    purchase.purchase_price,

    EXISTS (
        SELECT 1
        FROM checkinlog AS cl
        WHERE cl.tid = t.tid
    ) AS is_used

FROM ticket AS t

INNER JOIN reservation AS r
    ON r.reservation_id = t.reservation_id

INNER JOIN event AS e
    ON e.eid = r.event_id

INNER JOIN seatinventory AS si
    ON si.invid = t.invid

LEFT JOIN LATERAL (
    SELECT
        ri.price AS purchase_price

    FROM reservation_item AS ri

    WHERE
        ri.reservation_id = r.reservation_id
        AND ri.cat_id = si.catid

    ORDER BY ri.item_id ASC

    LIMIT 1
) AS purchase
    ON TRUE

WHERE
    t.tid = %s
    AND r.user_id = %s

FOR UPDATE OF t, r, si;
"""


GET_CANCELLATION_RULE = """
SELECT
    cr.rule_id,
    cr.organizer_id,

    cr.min_hours_before_event,
    cr.max_hours_before_event,

    cr.refund_percent,
    cr.can_cancel,

    cr.notes AS policy_notes,

    EXTRACT(
        EPOCH FROM (
            e.eventdate - NOW()
        )
    ) / 3600.0 AS remaining_hours

FROM event AS e

INNER JOIN cancellation_rule AS cr
    ON cr.organizer_id = e.organizer_id

WHERE
    e.eid = %s

    AND cr.is_active = TRUE

    AND (
        EXTRACT(
            EPOCH FROM (
                e.eventdate - NOW()
            )
        ) / 3600.0
    ) >= cr.min_hours_before_event

    AND (
        cr.max_hours_before_event IS NULL

        OR (
            EXTRACT(
                EPOCH FROM (
                    e.eventdate - NOW()
                )
            ) / 3600.0
        ) < cr.max_hours_before_event
    )

ORDER BY
    cr.min_hours_before_event DESC

LIMIT 1;
"""



GET_SUCCESSFUL_PAYMENT_FOR_UPDATE = """
SELECT
    id AS payment_id,
    reservation_id,
    amount,
    method,
    status AS payment_status,
    paid_at,
    refund_amount,
    refunded_at

FROM payment

WHERE
    reservation_id = %s
    AND LOWER(COALESCE(status, '')) = 'successful'

ORDER BY id DESC

LIMIT 1

FOR UPDATE;
"""



ENSURE_USER_WALLET = """
INSERT INTO wallet (
    user_id,
    balance
)
VALUES (
    %s,
    0
)

ON CONFLICT (user_id)
DO NOTHING;
"""



GET_USER_WALLET_FOR_UPDATE = """
SELECT
    wallet_id,
    user_id,
    balance

FROM wallet

WHERE user_id = %s

FOR UPDATE;
"""


CREDIT_WALLET = """
UPDATE wallet

SET
    balance = balance + %s,
    updated_at = NOW()

WHERE wallet_id = %s

RETURNING
    wallet_id,
    user_id,
    balance AS wallet_balance,
    updated_at;
"""


CANCEL_TICKET = """
UPDATE ticket

SET
    status = 'cancelled'

WHERE tid = %s

RETURNING
    tid AS ticket_id,
    status AS ticket_status;
"""


RELEASE_CANCELLED_TICKET_INVENTORY = """
UPDATE seatinventory

SET
    status = 'available',
    reservation_id = NULL,
    reservekey = NULL,
    held_until = NULL

WHERE invid = %s

RETURNING
    invid AS inventory_id,
    status AS inventory_status;
"""



CANCEL_RESERVATION = """
UPDATE reservation

SET
    status = 'cancelled'

WHERE reservation_id = %s

RETURNING
    reservation_id,
    status AS reservation_status;
"""


MARK_PAYMENT_AS_REFUNDED = """
UPDATE payment

SET
    status = 'refunded',
    refund_amount = %s,
    refunded_at = NOW()

WHERE id = %s

RETURNING
    id AS payment_id,
    status AS payment_status,
    refund_amount,
    refunded_at;
"""











#نمایش فهرست ورزشگاه‌ها به همراه شهر
SportTicket_VenueCatalogQuery = """
SELECT
    venue_id,
    name AS venue_name,
    city
FROM "Venue"
ORDER BY city, name;
"""

#نمایش فهرست شهرهای دارای ورزشگاه
SportTicket_CityCatalogQuery = """
SELECT DISTINCT city
FROM "Venue"
WHERE city IS NOT NULL
ORDER BY city;
"""

#نمایش فهرست تیم‌ها به همراه شهر
SportTicket_TeamCatalogQuery = """
SELECT
    team_id,
    name AS team_name,
    city
FROM "Team"
ORDER BY name;
"""

#نمایش فهرست رشته‌های ورزشی
SportTicket_SportCatalogQuery = """
SELECT
    sport_id,
    name AS sport_name
FROM "Sport"
ORDER BY name;
"""

#نمایش لیگ‌ها به همراه رشتهٔ ورزشی مربوطه
SportTicket_LeagueCatalogQuery = """
SELECT
    l.league_id,
    l.name AS league_name,
    s.name AS sport_name
FROM "League" AS l, "Sport" AS s
WHERE s.sport_id = l.sport_id
ORDER BY s.name, l.name;
"""

#نمایش فهرست مسابقات آینده
SportTicket_UpcomingMatchListQuery = """
SELECT
    e.event_id,
    s.name AS sport_name,
    l.name AS league_name,
    home.name AS home_team,
    away.name AS away_team,
    v.name AS venue_name,
    v.city,
    e.event_date,
    e.start_time
FROM "Event" AS e, "Sport" AS s, "League" AS l, "Venue" AS v, "Team" AS home, "Team" AS away
WHERE e.sport_id = s.sport_id
  AND e.league_id = l.league_id
  AND e.venue_id = v.venue_id
  AND e.home_team_id = home.team_id
  AND e.away_team_id = away.team_id
  AND e.event_date >= CURRENT_DATE
ORDER BY e.event_date, e.start_time;
"""

#جست‌وجوی مسابقات برگزارشونده در یک شهر مشخص
SportTicket_CityMatchFinderQuery = """
SELECT
    e.event_id,
    home.name AS home_team_name,
    away.name AS away_team_name,
    v.name AS venue_name,
    v.city,
    e.event_date,
    e.start_time
FROM "Event" AS e, "Venue" AS v, "Team" AS home, "Team" AS away
WHERE e.venue_id = v.venue_id
  AND e.home_team_id = home.team_id
  AND e.away_team_id = away.team_id
  AND v.city = %s
  AND e.status = 'scheduled'
ORDER BY e.event_date, e.start_time;
"""

#جست‌وجوی مسابقات یک تیم مشخص
SportTicket_TeamMatchFinderQuery = """
SELECT
    e.event_id,
    home.name AS home_team,
    away.name AS away_team,
    e.event_date,
    e.start_time,
    v.name AS venue_name,
    v.city
FROM "Event" AS e, "Team" AS home, "Team" AS away, "Venue" AS v
WHERE e.home_team_id = home.team_id
  AND e.away_team_id = away.team_id
  AND e.venue_id = v.venue_id
  AND (home.name LIKE '%' || :team_name || '%'
       OR away.name LIKE '%' || :team_name || '%')
ORDER BY e.event_date, e.start_time;
"""

#جست‌وجوی مسابقات مربوط به یک رشتهٔ ورزشی مشخص
SportTicket_SportMatchFinderQuery = """
SELECT
    e.event_id,
    s.name AS sport_name,
    home.name AS home_team,
    away.name AS away_team,
    l.name AS league_name,
    v.name AS venue_name,
    v.city,
    e.event_date,
    e.start_time
FROM "Event" AS e, "Sport" AS s, "Team" AS home, "Team" AS away, "League" AS l, "Venue" AS v
WHERE e.sport_id = s.sport_id
  AND e.home_team_id = home.team_id
  AND e.away_team_id = away.team_id
  AND e.league_id = l.league_id
  AND e.venue_id = v.venue_id
  AND s.name = :sport_name
ORDER BY e.event_date, e.start_time;
"""

#نمایش کاربرانی که هیچ رزروی ثبت نکرده‌اند
SportTicket_UsersWithoutReservationQuery = """
SELECT u.first_name, u.last_name
FROM Users u
WHERE NOT EXISTS (
    SELECT 1
    FROM Reservation r
    WHERE r.user_id = u.user_id
);
"""

#نمایش کاربرانی که حداقل یک رزرو فعال دارند
SportTicket_UsersWithActiveReservationQuery = """
SELECT u.first_name, u.last_name
FROM Users u
WHERE EXISTS (
    SELECT 1
    FROM Reservation r
    WHERE r.user_id = u.user_id
      AND r.status = 'active'
);
"""

#محاسبهٔ مجموع پرداخت هر کاربر به تفکیک ماه
SportTicket_UserMonthlyPaymentQuery = """
SELECT r.user_id, p.payment_month, SUM(p.amount) AS total_paid
FROM Reservation r, Payment p
WHERE r.reservation_id = p.reservation_id
GROUP BY r.user_id, p.payment_month
ORDER BY r.user_id, p.payment_month;
"""

#نمایش کاربرانی که در هر شهر دقیقاً یک خرید موفق داشته‌اند
SportTicket_OnePurchasePerCityQuery = """
SELECT r.user_id, v.city
FROM Reservation r, Event e, Venue v
WHERE r.event_id = e.event_id
  AND e.venue_id = v.venue_id
  AND r.status = 'active'
GROUP BY r.user_id, v.city
HAVING COUNT(r.reservation_id) = 1;
"""

#نمایش اطلاعات خریدار آخرین بلیط ثبت‌شده
SportTicket_LatestTicketBuyerQuery = """
SELECT u.first_name, u.last_name, r.created_at
FROM Users u, Reservation r
WHERE u.user_id = r.user_id
  AND r.created_at = (
      SELECT MAX(created_at)
      FROM Reservation
  );
"""

#نمایش کاربرانی که مجموع پرداختشان بیشتر از میانگین کل پرداخت‌ها است
SportTicket_HighSpendingUsersQuery = """
SELECT r.user_id, SUM(p.amount) AS total_spent
FROM Reservation r, Payment p
WHERE r.reservation_id = p.reservation_id
GROUP BY r.user_id
HAVING SUM(p.amount) > (
    SELECT AVG(amount)
    FROM Payment
);
"""

#محاسبهٔ تعداد بلیط‌های فروخته‌شده به تفکیک رشتهٔ ورزشی
SportTicket_TicketsSoldPerSportQuery = """
SELECT s.name AS sport_name, COUNT(r.reservation_id) AS tickets_sold
FROM Reservation r, Event e, Sport s
WHERE r.event_id = e.event_id
  AND e.sport_id = s.sport_id
  AND r.status = 'active'
GROUP BY s.sport_id, s.name;
"""

#نمایش کاربران با بیشترین تعداد خرید در یک بازهٔ زمانی مشخص
SportTicket_TopBuyersInPeriodQuery = """
SELECT u.first_name, u.last_name, COUNT(r.reservation_id) AS ticket_count
FROM Users u, Reservation r
WHERE u.user_id = r.user_id
  AND r.created_at >= '2026-08-04 00:00:00'
GROUP BY u.user_id, u.first_name, u.last_name
ORDER BY ticket_count DESC;
"""

#محاسبهٔ آمار فروش بلیط در شهرهای استان تهران
SportTicket_TehranProvinceSalesQuery = """
SELECT v.city, COUNT(r.reservation_id) AS tickets_sold
FROM Reservation r, Event e, Venue v
WHERE r.event_id = e.event_id
  AND e.venue_id = v.venue_id
  AND v.province = 'تهران'
  AND r.status = 'active'
GROUP BY v.city;
"""

#نمایش شهرهای مسابقاتی که قدیمی‌ترین کاربر سامانه برای آن‌ها رزرو داشته است
SportTicket_OldestUserVisitedCitiesQuery = """
SELECT DISTINCT v.city
FROM Reservation r, Event e, Venue v
WHERE r.event_id = e.event_id
  AND e.venue_id = v.venue_id
  AND r.user_id = (
      SELECT user_id
      FROM Users
      WHERE created_at = (
          SELECT MIN(created_at)
          FROM Users
      )
  );
"""

#نمایش فهرست اعضای تیم پشتیبانی سامانه
SportTicket_SupportStaffListQuery = """
SELECT first_name, last_name, email
FROM Users
WHERE role = 'support'
ORDER BY last_name, first_name;
"""

#نمایش کاربران وفادار با حداقل دو خرید فعال
SportTicket_LoyalUsersQuery = """
SELECT u.first_name, u.last_name, COUNT(r.reservation_id) AS total_tickets
FROM Users u, Reservation r
WHERE u.user_id = r.user_id
  AND r.status = 'active'
GROUP BY u.user_id, u.first_name, u.last_name
HAVING COUNT(r.reservation_id) >= 2;
"""

#نمایش کاربرانی که حداکثر دو بلیط فوتبال خریده‌اند
SportTicket_UsersWithAtMostTwoFootballTicketsQuery = """
SELECT u.first_name, u.last_name, COUNT(r.reservation_id) AS ticket_count
FROM Users u, Reservation r, Event e, Sport s
WHERE u.user_id = r.user_id
  AND r.event_id = e.event_id
  AND e.sport_id = s.sport_id
  AND s.name = 'فوتبال'
  AND r.status = 'active'
GROUP BY u.user_id, u.first_name, u.last_name
HAVING COUNT(r.reservation_id) <= 2;
"""

#نمایش کاربرانی که از تمام رشته‌های فوتبال، والیبال و بسکتبال بلیط خریده‌اند
SportTicket_AllSportsBuyersQuery = """
SELECT u.first_name, u.last_name
FROM Users u, Reservation r, Event e, Sport s
WHERE u.user_id = r.user_id
  AND r.event_id = e.event_id
  AND e.sport_id = s.sport_id
  AND s.name IN ('فوتبال', 'والیبال', 'بسکتبال')
  AND r.status = 'active'
GROUP BY u.user_id, u.first_name, u.last_name
HAVING COUNT(DISTINCT s.sport_id) = 3;
"""

#نمایش رزروهای ثبت‌شده در تاریخ مشخص
SportTicket_TodayReservationsQuery = """
SELECT reservation_id, user_id, event_id, created_at
FROM Reservation
WHERE created_at >= '2026-08-11 00:00:00'
  AND created_at <= '2026-08-11 23:59:59'
ORDER BY created_at ASC;
"""

#نمایش مسابقه یا مسابقات با دومین میزان فروش بلیط
SportTicket_SecondBestSellingEventQuery = """
SELECT event_id, COUNT(reservation_id) AS ticket_count
FROM Reservation
WHERE status = 'active'
GROUP BY event_id
HAVING COUNT(reservation_id) = (
    SELECT MAX(sub.sales_count)
    FROM (
        SELECT COUNT(r2.reservation_id) AS sales_count
        FROM Reservation r2
        WHERE r2.status = 'active'
        GROUP BY r2.event_id
    ) sub
    WHERE sub.sales_count < (
        SELECT MAX(all_sales.sales_count)
        FROM (
            SELECT COUNT(r3.reservation_id) AS sales_count
            FROM Reservation r3
            WHERE r3.status = 'active'
            GROUP BY r3.event_id
        ) all_sales
    )
);
"""

#نمایش عضو پشتیبانی با بیشترین تعداد رزرو لغوشده
SportTicket_SupportWithMostCancellationsQuery = """
SELECT u.first_name, u.last_name, COUNT(r.reservation_id) AS cancellation_count
FROM Users u, Reservation r
WHERE u.user_id = r.user_id
  AND u.role = 'support'
  AND r.status = 'cancelled'
GROUP BY u.user_id, u.first_name, u.last_name
HAVING COUNT(r.reservation_id) = (
    SELECT MAX(temp.cxl_count)
    FROM (
        SELECT COUNT(r2.reservation_id) AS cxl_count
        FROM Users u2, Reservation r2
        WHERE u2.user_id = r2.user_id
          AND u2.role = 'support'
          AND r2.status = 'cancelled'
        GROUP BY u2.user_id
    ) temp
);
"""

#تغییر نام خانوادگی کاربر دارای بیشترین لغو رزرو به Reddington
SportTicket_UpdateReddingtonLastNameQuery = """
UPDATE Users
SET last_name = 'Reddington'
WHERE user_id = (
    SELECT r.user_id
    FROM Reservation r
    WHERE r.status = 'cancelled'
    GROUP BY r.user_id
    HAVING COUNT(r.reservation_id) = (
        SELECT MAX(temp.cxl_count)
        FROM (
            SELECT COUNT(r2.reservation_id) AS cxl_count
            FROM Reservation r2
            WHERE r2.status = 'cancelled'
            GROUP BY r2.user_id
        ) temp
    )
);
"""

#حذف رزروهای لغوشدهٔ کاربر با نام خانوادگی Reddington
SportTicket_DeleteReddingtonCancelledReservationsQuery = """
DELETE FROM Reservation
WHERE status = 'cancelled'
  AND user_id IN (
      SELECT user_id
      FROM Users
      WHERE last_name = 'Reddington'
  );
"""

#حذف تمام رزروهای لغوشده از سامانه
SportTicket_DeleteAllCancelledReservationsQuery = """
DELETE FROM Reservation
WHERE status = 'cancelled';
"""

#اعمال ۱۰ درصد تخفیف برای مسابقات ورزشگاه آزادی در یک تاریخ مشخص
SportTicket_AzadiStadiumDiscountQuery = """
UPDATE Event
SET ticket_price = ticket_price * 0.90
WHERE venue_id IN (
    SELECT venue_id
    FROM Venue
    WHERE name = 'ورزشگاه آزادی'
)
AND event_date >= '2026-08-10 00:00:00'
AND event_date <= '2026-08-10 23:59:59';
"""

#نمایش موضوع و تعداد گزارش‌ها برای مسابقه‌ای با بیشترین گزارش
SportTicket_MostReportedEventSubjectsQuery = """
SELECT rep.subject, COUNT(rep.report_id) AS report_count
FROM Report rep
WHERE rep.event_id = (
    SELECT r.event_id
    FROM Report r
    GROUP BY r.event_id
    HAVING COUNT(r.report_id) = (
        SELECT MAX(temp.rep_count)
        FROM (
            SELECT COUNT(r2.report_id) AS rep_count
            FROM Report r2
            GROUP BY r2.event_id
        ) temp
    )
)
GROUP BY rep.subject;
"""