from typing import Any
from pydantic import BaseModel
from schemas.block import Block
from schemas.transaction import Transaction
from utils.utils import get_config

class Blockchain(BaseModel):
    chain: list[Block] = []
    current_transactions: list[Transaction] = []

    def create_genesis_block(self) -> None:
        self.create_block(previous_hash='1')

    # Create genesis block if blockchain is empty
    def model_post_init(self, __context: Any) -> None:
        if len(self.chain) == 0: 
            genesis_block = self.create_block(previous_hash='1')
            self.add_block(genesis_block)

    def create_block(self, previous_hash=None) -> Block:
        print("Creating a new block...")
        
        if previous_hash is None:
            previous_hash = self.last_block.hash

        block = Block(
            index=len(self.chain) + 1,
            hash="", # will be calculated later
            transactions=self.current_transactions,
            previous_block_hash=previous_hash
        )

        self.current_transactions = []
        return block

    def add_block(self, block: Block) -> None:
        self.chain.append(block)
    
    def add_transaction(self, sender: str, recipient: str, data: str, signature: str) -> None:
        transaction = Transaction(
            sender=sender,
            recipient=recipient,
            data=data,
            signature=signature,
        )

        self.current_transactions.append(transaction)

        #TODO: delete this later
        # if len(self.current_transactions) >= get_config()["max_block_size"]:
        #     self.create_block(self.last_block.hash)

    def should_mine_block(self) -> bool:
        return len(self.current_transactions) >= get_config()["max_block_size"]

    @property
    def last_block(self) -> Block:
        return self.chain[-1]