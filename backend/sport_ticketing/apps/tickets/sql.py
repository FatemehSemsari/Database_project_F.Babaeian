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