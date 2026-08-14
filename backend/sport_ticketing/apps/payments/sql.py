GET_RESERVATION_FOR_PAYMENT = """
SELECT
    r.reservation_id,
    r.user_id,
    r.event_id,
    r.status,
    r.total_amount,
    r.reserved_at,
    r.expires_at,
    r.paid_at,

    (
        r.expires_at IS NOT NULL
        AND r.expires_at <= NOW()
    ) AS is_expired

FROM reservation AS r

WHERE
    r.reservation_id = %s
    AND r.user_id = %s

FOR UPDATE;
"""


GET_RESERVATION_INVENTORIES_FOR_UPDATE = """
SELECT
    si.invid AS inventory_id,
    si.seatid AS seat_id,
    si.status AS inventory_status,
    si.reservation_id AS hold_reservation_id,
    si.held_until,

    (
        LOWER(COALESCE(si.status, '')) = 'held'
        AND si.reservation_id = %s
        AND si.held_until IS NOT NULL
        AND si.held_until > NOW()
    ) AS valid_hold

FROM reservation_seat AS rs

INNER JOIN seatinventory AS si
    ON si.invid = rs.inventory_id

WHERE
    rs.reservation_id = %s

ORDER BY
    si.invid

FOR UPDATE OF si;
"""


EXPIRE_RESERVATION = """
UPDATE reservation
SET
    status = 'expired'
WHERE reservation_id = %s;
"""


RELEASE_RESERVATION_INVENTORY = """
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
    AND LOWER(COALESCE(si.status, '')) = 'held';
"""


CREATE_SUCCESSFUL_PAYMENT = """
INSERT INTO payment (
    reservation_id,
    amount,
    method,
    status,
    created_at,
    paid_at,
    transaction_ref
)
VALUES (
    %s,
    %s,
    %s,
    'successful',
    NOW(),
    NOW(),
    %s
)
RETURNING
    id AS payment_id,
    reservation_id,
    amount,
    method,
    status AS payment_status,
    paid_at,
    transaction_ref;
"""


MARK_RESERVATION_AS_PAID = """
UPDATE reservation
SET
    status = 'paid',
    paid_at = NOW()
WHERE reservation_id = %s
RETURNING
    status AS reservation_status,
    paid_at;
"""


MARK_RESERVATION_INVENTORY_AS_SOLD = """
UPDATE seatinventory AS si
SET
    status = 'sold',
    reservation_id = NULL,
    reservekey = NULL,
    held_until = NULL

FROM reservation_seat AS rs

WHERE
    rs.reservation_id = %s
    AND rs.inventory_id = si.invid;
"""


ISSUE_RESERVATION_TICKETS = """
INSERT INTO ticket (
    reservation_id,
    invid,
    serialnum,
    status,
    issuedate
)
SELECT
    rs.reservation_id,
    rs.inventory_id,
    nextval('ticket_serial_number_seq')::INTEGER,
    'valid',
    NOW()

FROM reservation_seat AS rs

WHERE
    rs.reservation_id = %s

ORDER BY
    rs.inventory_id

RETURNING
    tid AS ticket_id,
    invid AS inventory_id,
    serialnum AS serial_number,
    status,
    issuedate AS issue_date;
"""



