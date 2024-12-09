import json

from clients.redis import RedisClient

from schemas.blockchain import Blockchain
from schemas.block import Block
from schemas.transaction import Transaction

db_client = RedisClient.get_client()

def get_blockchain():
    blockchain_raw = db_client.get('blockchan')
    return Blockchain(**json.loads(blockchain_raw))

def set_blockchain(blockchain: Blockchain):
    db_client.set('blockchan', blockchain.model_dump_json())

def save_blockchain(blockchain: Blockchain):
    db_client.set('blockchan', blockchain.model_dump_json())

def save_transaction(transaction: Transaction):
    blockchain = get_blockchain()
    blockchain.add_transaction(transaction.sender, transaction.recipient, transaction.data, transaction.signature)
    save_blockchain(blockchain)

    return "Transaction added to the blockchain"

def save_block(block: Block):
    blockchain = get_blockchain()
    blockchain.add_block(block)
    save_blockchain(blockchain)

    return "Block added to the blockchain"
