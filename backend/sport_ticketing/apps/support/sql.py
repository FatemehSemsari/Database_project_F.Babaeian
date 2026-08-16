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
WITH updated_report AS (
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
        reportid,
        user_id,
        tid,
        reservation_id,
        subject,
        message,
        status,
        support_response,
        reviewed_by,
        reviewed_at
)

SELECT
    ur.reportid AS report_id,

    ur.user_id,

    u.first_name,
    u.last_name,
    u.email,
    u.phone,

    ur.tid AS ticket_id,
    ur.reservation_id,

    ur.subject AS issue_type,
    ur.message,

    ur.status,
    ur.support_response,

    ur.reviewed_by,
    ur.reviewed_at,

    reviewer.first_name
        AS reviewer_first_name,

    reviewer.last_name
        AS reviewer_last_name

FROM updated_report AS ur

INNER JOIN users AS u
    ON u.id = ur.user_id

LEFT JOIN users AS reviewer
    ON reviewer.id = ur.reviewed_by;
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


