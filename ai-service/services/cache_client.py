import redis

class CacheClient:
    def __init__(self):
        self.client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

        self.hit = 0
        self.miss = 0

    def get(self, key):
        value = self.client.get(key)
        if value:
            self.hit += 1
            print("cache hit")
        else:
            self.miss += 1
            print("cache miss")
        return value

    def set(self, key, value, ttl=900):  # 15 min
        self.client.setex(key, ttl, value)

    def get_stats(self):
        return {
            "hits": self.hit,
            "miss": self.miss
        }