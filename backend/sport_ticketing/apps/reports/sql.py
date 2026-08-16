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


LIST_USER_REPORTS = """
SELECT
    rp.reportid AS report_id,
    rp.user_id,
    rp.tid AS ticket_id,
    rp.reservation_id,
    rp.subject AS issue_type,
    rp.message,
    rp.status,
    rp.support_response,
    rp.reviewed_at

FROM report AS rp

WHERE
    rp.user_id = %s

ORDER BY
    rp.reportid DESC;
"""