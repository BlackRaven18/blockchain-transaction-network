import redis
from schemas.blockchain import Blockchain
from config import args

class RedisClient:
    _client = None

    @classmethod
    def __init_db(cls):
        if cls._client is not None:
            cls._client.set('blockchan', Blockchain().model_dump_json())

    @classmethod
    def get_client(cls):
        if cls._client is None:
            host = args.db_host
            port = args.db_port
            try:
                cls._client = redis.Redis(host=host, port=port, decode_responses=True)
                cls.__init_db()
            except ConnectionError as e:
                print(f"Error connecting to Redis server: {e}")
        return cls._client