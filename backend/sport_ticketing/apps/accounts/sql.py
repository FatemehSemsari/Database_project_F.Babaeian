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