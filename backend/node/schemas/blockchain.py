from typing import Any
from pydantic import BaseModel
from schemas.block import Block
from schemas.transaction import Transaction
from constants import MAX_BLOCK_SIZE

class Blockchain(BaseModel):
    chain: list[Block] = []
    current_transactions: list[Transaction] = []

    def create_genesis_block(self) -> None:
        self.create_block(previous_hash='1')


    # Create genesis block if blockchain is empty
    def model_post_init(self, __context: Any) -> None:
        if len(self.chain) == 0: 
            self.create_block(previous_hash='1')

    def create_block(self, previous_hash=None) -> Block:
        print("Creating a new block...")
        block = Block(
            index=len(self.chain) + 1,
            hash=previous_hash,
            transactions=self.current_transactions,
            previous_block_hash=previous_hash
        )

        self.current_transactions = []
        self.chain.append(block)
        return block
    
    def add_transaction(self, sender: str, recipient: str, data: str, signature: str) -> None:
        transaction = Transaction(
            sender=sender,
            recipient=recipient,
            data=data,
            signature=signature,
        )

        self.current_transactions.append(transaction)

        if len(self.current_transactions) >= MAX_BLOCK_SIZE:
            print("No to tu to mnie kurde nie ma no nie...")
            self.create_block(self.last_block.hash)

    @property
    def last_block(self) -> Block:
        return self.chain[-1]