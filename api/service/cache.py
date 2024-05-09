import redis

redis_client = None

def init_cache(app):
    global redis_client
    redis_client = redis.StrictRedis(
        host='localhost',
        port=6379,
        db=0,
        decode_responses=True
    )

def set_key(key, value, expire=None):
    """Set a value in the Redis cache."""
    if expire:
        redis_client.setex(key, expire, value)
    else:
        redis_client.set(key, value)

def get_key(key):
    """Get a value from the Redis cache."""
    return redis_client.get(key)
