from clients.redis_client import RedisClient
from schemas.blockchain import Blockchain
import json

db_client = RedisClient.get_client()

def get_blockchain():
    blockchain_raw = db_client.get('blockchan')
    return Blockchain(**json.loads(blockchain_raw))

def set_blockchain(blockchain: Blockchain):
    db_client.set('blockchan', blockchain.model_dump_json())