import redis

class RedisClient:
    def __init__(self, host, port):
        self.client = redis.Redis(host=host, port=port)

    def set(self, key, value):
        self.client.set(key, value)

    def get(self, key):
        return self.client.get(key)