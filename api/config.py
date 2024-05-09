import redis

def get_cache():
    cache = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    # song_schema = (
    #     TextField("$.SONG_NAME", as_name="SONG_NAME")
    # )

    return cache

cache = get_cache()