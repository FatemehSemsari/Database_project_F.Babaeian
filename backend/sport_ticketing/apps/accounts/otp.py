import random
from django.conf import settings
import redis


redis_client = redis.Redis(
    host=getattr(settings, "REDIS_HOST", "localhost"),
    port=getattr(settings, "REDIS_PORT", 6379),
    db=getattr(settings, "REDIS_DB", 0),
    decode_responses=True,
)


def get_signup_target(email=None, phone=None):
    if phone:
        return "phone", phone
    return "email", email


def generate_otp_code():
    return str(random.randint(100000, 999999))


def build_signup_otp_key(target_type, target_value):
    return f"otp:signup:{target_type}:{target_value}"


def create_signup_otp(email=None, phone=None):
    target_type, target_value = get_signup_target(email=email, phone=phone)
    code = generate_otp_code()
    key = build_signup_otp_key(target_type, target_value)
    redis_client.setex(
        key,
        getattr(settings, "OTP_TTL_SECONDS", 120),
        code,
    )
    return {
        "target_type": target_type,
        "target_value": target_value,
        "otp_code": code,
    }


def verify_signup_otp(email=None, phone=None, otp_code=None):
    target_type, target_value = get_signup_target(email=email, phone=phone)
    key = build_signup_otp_key(target_type, target_value)
    saved_code = redis_client.get(key)
    if not saved_code:
        return False, target_type
    if saved_code != otp_code:
        return False, target_type
    redis_client.delete(key)
    return True, target_type


def get_login_target(email=None, phone=None):
    if phone:
        return "phone", phone
    return "email", email

def build_login_otp_key(target_type, target_value):
    return f"otp:login:{target_type}:{target_value}"

def create_login_otp(email=None, phone=None):
    target_type, target_value = get_login_target(email=email, phone=phone)
    code = generate_otp_code()
    key = build_login_otp_key(target_type, target_value)
    redis_client.setex(
        key,
        getattr(settings, "OTP_TTL_SECONDS", 120),
        code,
    )
    return {
        "target_type": target_type,
        "target_value": target_value,
        "otp_code": code,
    }

def verify_login_otp(email=None, phone=None, otp_code=None):
    target_type, target_value = get_login_target(email=email, phone=phone)
    key = build_login_otp_key(target_type, target_value)
    saved_code = redis_client.get(key)
    if not saved_code:
        return False, target_type
    if saved_code != otp_code:
        return False, target_type
    redis_client.delete(key)
    return True, target_type