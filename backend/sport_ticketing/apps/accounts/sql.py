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
    is_active,
    created_at
FROM users
WHERE id = %s
LIMIT 1;
"""