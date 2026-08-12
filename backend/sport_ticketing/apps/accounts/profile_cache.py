import json
import redis
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.dateparse import parse_datetime


redis_client = redis.Redis(
    host=getattr(settings, "REDIS_HOST", "localhost"),
    port=getattr(settings, "REDIS_PORT", 6379),
    db=getattr(settings, "REDIS_DB", 0),
    decode_responses=True,
)


def build_profile_cache_key(user_id):
    return f"profile:user:{user_id}"


def get_cached_profile(user_id):
    key = build_profile_cache_key(user_id)
    try:
        cached_data = redis_client.get(key)
    except redis.RedisError:
        return None
    if not cached_data:
        return None
    try:
        profile = json.loads(cached_data)
    except json.JSONDecodeError:
        redis_client.delete(key)
        return None
    for field_name in ("created_at", "updated_at"):
        value = profile.get(field_name)
        if isinstance(value, str):
            parsed_value = parse_datetime(value)
            if parsed_value is not None:
                profile[field_name] = parsed_value
    return profile


def cache_profile(profile):
    user_id = profile["id"]
    key = build_profile_cache_key(user_id)
    try:
        redis_client.setex(
            key,
            getattr(
                settings,
                "PROFILE_CACHE_TTL_SECONDS",
                300,
            ),
            json.dumps(
                profile,
                cls=DjangoJSONEncoder,
            ),
        )
    except redis.RedisError:
        pass


def delete_cached_profile(user_id):
    key = build_profile_cache_key(user_id)
    try:
        redis_client.delete(key)
    except redis.RedisError:
        pass