import hashlib
import json
from datetime import date, datetime, time
from decimal import Decimal
import redis
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder


redis_client = redis.Redis(
    host=getattr(
        settings,
        "REDIS_HOST",
        "localhost",
    ),
    port=getattr(
        settings,
        "REDIS_PORT",
        6379,
    ),
    db=getattr(
        settings,
        "REDIS_DB",
        0,
    ),
    decode_responses=True,
)


SEARCH_CACHE_VERSION_KEY = "ticket-search:version"


def normalize_cache_value(value):
    if isinstance(value, (date, datetime, time, Decimal)):
        return str(value)
    return value


def normalize_filters(filters):
    return {
        key: normalize_cache_value(value)
        for key, value in sorted(filters.items())
    }


def get_search_cache_version():
    try:
        version = redis_client.get(SEARCH_CACHE_VERSION_KEY)
        if version is None:
            redis_client.set(
                SEARCH_CACHE_VERSION_KEY,
                "1",
            )
            return 1
        return int(version)
    except (redis.RedisError, TypeError, ValueError):
        return 1


def build_ticket_search_cache_key(filters):
    normalized_filters = normalize_filters(filters)
    serialized_filters = json.dumps(
        normalized_filters,
        sort_keys=True,
        ensure_ascii=False,
    )
    filters_hash = hashlib.sha256(
        serialized_filters.encode("utf-8")
    ).hexdigest()
    version = get_search_cache_version()
    return (
        f"ticket-search:"
        f"v{version}:"
        f"{filters_hash}"
    )


def get_cached_ticket_search(filters):
    key = build_ticket_search_cache_key(filters)
    try:
        cached_data = redis_client.get(key)
    except redis.RedisError:
        return None
    if not cached_data:
        return None
    try:
        return json.loads(cached_data)
    except json.JSONDecodeError:
        try:
            redis_client.delete(key)
        except redis.RedisError:
            pass
        return None


def cache_ticket_search(filters, results):
    key = build_ticket_search_cache_key(filters)
    try:
        redis_client.setex(
            key,
            getattr(
                settings,
                "TICKET_SEARCH_CACHE_TTL_SECONDS",
                30,
            ),
            json.dumps(
                results,
                cls=DjangoJSONEncoder,
                ensure_ascii=False,
            ),
        )
    except redis.RedisError:
        pass


def invalidate_ticket_search_cache():
    try:
        redis_client.incr(
            SEARCH_CACHE_VERSION_KEY
        )
    except redis.RedisError:
        pass