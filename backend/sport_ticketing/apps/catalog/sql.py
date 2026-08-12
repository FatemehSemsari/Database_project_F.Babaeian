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