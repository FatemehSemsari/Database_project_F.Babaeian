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