import json
import random

import redis
from django.conf import settings


redis_client = redis.Redis(
    host=getattr(settings, "REDIS_HOST", "localhost"),
    port=getattr(settings, "REDIS_PORT", 6379),
    db=getattr(settings, "REDIS_DB", 0),
    decode_responses=True,
)


def generate_otp_code():
    return str(random.randint(100000, 999999))


def build_attempts_key(otp_key):
    return f"{otp_key}:attempts"


def build_cooldown_key(otp_key):
    return f"{otp_key}:cooldown"


def store_otp_with_limits(otp_key, value):
    cooldown_key = build_cooldown_key(otp_key)
    attempts_key = build_attempts_key(otp_key)
    remaining_cooldown = redis_client.ttl(cooldown_key)
    if remaining_cooldown > 0:
        return {
            "created": False,
            "retry_after": remaining_cooldown,
        }
    otp_ttl = getattr(
        settings,
        "OTP_TTL_SECONDS",
        120,
    )
    cooldown_seconds = getattr(
        settings,
        "OTP_RESEND_COOLDOWN_SECONDS",
        60,
    )
    pipeline = redis_client.pipeline()
    pipeline.setex(
        otp_key,
        otp_ttl,
        value,
    )
    pipeline.setex(
        cooldown_key,
        cooldown_seconds,
        "1",
    )
    pipeline.delete(attempts_key)
    pipeline.execute()
    return {
        "created": True,
        "retry_after": 0,
    }


def register_failed_otp_attempt(otp_key):
    attempts_key = build_attempts_key(otp_key)
    attempts = redis_client.incr(attempts_key)
    if attempts == 1:
        remaining_otp_time = redis_client.ttl(otp_key)
        if remaining_otp_time <= 0:
            remaining_otp_time = getattr(
                settings,
                "OTP_TTL_SECONDS",
                120,
            )
        redis_client.expire(
            attempts_key,
            remaining_otp_time,
        )
    max_attempts = getattr(
        settings,
        "OTP_MAX_ATTEMPTS",
        5,
    )
    if attempts >= max_attempts:
        redis_client.delete(
            otp_key,
            attempts_key,
        )
    return attempts


def clear_otp_value_and_attempts(otp_key):
    redis_client.delete(
        otp_key,
        build_attempts_key(otp_key),
    )


# Signup OTP

def get_signup_target(email=None, phone=None):
    if phone:
        return "phone", phone
    return "email", email


def build_signup_otp_key(target_type, target_value):
    return f"otp:signup:{target_type}:{target_value}"


def create_signup_otp(email=None, phone=None):
    target_type, target_value = get_signup_target(
        email=email,
        phone=phone,
    )
    code = generate_otp_code()
    key = build_signup_otp_key(
        target_type,
        target_value,
    )
    store_result = store_otp_with_limits(
        otp_key=key,
        value=code,
    )
    return {
        "created": store_result["created"],
        "retry_after": store_result["retry_after"],
        "target_type": target_type,
        "target_value": target_value,
        "otp_code": code if store_result["created"] else None,
    }


def verify_signup_otp(
    email=None,
    phone=None,
    otp_code=None,
):
    target_type, target_value = get_signup_target(
        email=email,
        phone=phone,
    )
    key = build_signup_otp_key(
        target_type,
        target_value,
    )
    saved_code = redis_client.get(key)
    if not saved_code:
        return False, target_type
    if saved_code != otp_code:
        register_failed_otp_attempt(key)
        return False, target_type
    return True, target_type


def delete_signup_otp(email=None, phone=None):
    target_type, target_value = get_signup_target(
        email=email,
        phone=phone,
    )
    key = build_signup_otp_key(
        target_type,
        target_value,
    )
    clear_otp_value_and_attempts(key)

# Login OTP

def get_login_target(email=None, phone=None):
    if phone:
        return "phone", phone
    return "email", email


def build_login_otp_key(target_type, target_value):
    return f"otp:login:{target_type}:{target_value}"


def create_login_otp(email=None, phone=None):
    target_type, target_value = get_login_target(
        email=email,
        phone=phone,
    )
    code = generate_otp_code()
    key = build_login_otp_key(
        target_type,
        target_value,
    )
    store_result = store_otp_with_limits(
        otp_key=key,
        value=code,
    )
    return {
        "created": store_result["created"],
        "retry_after": store_result["retry_after"],
        "target_type": target_type,
        "target_value": target_value,
        "otp_code": code if store_result["created"] else None,
    }


def verify_login_otp(
    email=None,
    phone=None,
    otp_code=None,
):
    target_type, target_value = get_login_target(
        email=email,
        phone=phone,
    )
    key = build_login_otp_key(
        target_type,
        target_value,
    )
    saved_code = redis_client.get(key)
    if not saved_code:
        return False, target_type
    if saved_code != otp_code:
        register_failed_otp_attempt(key)
        return False, target_type
    clear_otp_value_and_attempts(key)
    return True, target_type



# Contact-change OTP

def build_contact_change_otp_key(
    user_id,
    identifier_type,
):
    return (
        f"otp:contact-change:"
        f"{user_id}:{identifier_type}"
    )


def create_contact_change_otp(
    user_id,
    identifier_type,
    new_identifier,
):
    code = generate_otp_code()
    key = build_contact_change_otp_key(
        user_id=user_id,
        identifier_type=identifier_type,
    )
    value = json.dumps({
        "code": code,
        "new_identifier": new_identifier,
    })
    store_result = store_otp_with_limits(
        otp_key=key,
        value=value,
    )
    return {
        "created": store_result["created"],
        "retry_after": store_result["retry_after"],
        "target_type": identifier_type,
        "target_value": new_identifier,
        "otp_code": code if store_result["created"] else None,
    }


def verify_contact_change_otp(
    user_id,
    identifier_type,
    new_identifier,
    otp_code,
):
    key = build_contact_change_otp_key(
        user_id=user_id,
        identifier_type=identifier_type,
    )
    saved_value = redis_client.get(key)
    if not saved_value:
        return False
    try:
        otp_data = json.loads(saved_value)
    except json.JSONDecodeError:
        clear_otp_value_and_attempts(key)
        return False
    if otp_data.get("new_identifier") != new_identifier:
        register_failed_otp_attempt(key)
        return False
    if otp_data.get("code") != otp_code:
        register_failed_otp_attempt(key)
        return False
    return True


def delete_contact_change_otp(
    user_id,
    identifier_type,
):
    key = build_contact_change_otp_key(
        user_id=user_id,
        identifier_type=identifier_type,
    )
    clear_otp_value_and_attempts(key)