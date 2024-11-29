import redis
from schemas.blockchain import Blockchain
from args import args

class RedisClient:
    _client = None

    @classmethod
    def __init_db(cls):
        print("Initializing Redis database...")
        if cls._client is not None:
            blockchain = Blockchain()
            cls._client.set('blockchan', blockchain.model_dump_json())

    @classmethod
    def get_client(cls):
        if cls._client is None:
            host = args.db_host
            port = args.db_port
            index = args.db_index
            try:
                cls._client = redis.Redis(host=host, port=port, db=index, decode_responses=True)
                cls.__init_db()
            except ConnectionError as e:
                print(f"Error connecting to Redis server: {e}")
        return cls._client