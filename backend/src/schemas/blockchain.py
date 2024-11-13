from typing import Any
from pydantic import BaseModel
from schemas.block import Block
from schemas.transaction import Transaction
from constants import MAX_BLOCK_SIZE


class Blockchain(BaseModel):
    chain: list[Block] = []
    current_transactions: list[Transaction] = []

    def model_post_init(self, __context: Any) -> None:
        self.create_block(previous_hash='1')

    def create_block(self, previous_hash=None) -> Block:
        block = Block(
            index=len(self.chain) + 1,
            hash=previous_hash,
            transactions=self.current_transactions,
            previous_block_hash=previous_hash
        )

        self.current_transactions = []
        self.chain.append(block)
        return block
    
    def add_transaction(self, sender: str, recipient: str, data: str) -> None:
        transaction = Transaction(
            sender=sender,
            recipient=recipient,
            data=data
        )

        self.current_transactions.append(transaction)

        if len(self.current_transactions) >= MAX_BLOCK_SIZE:
            self.create_block(self.last_block.hash)

    @property
    def last_block(self) -> Block:
        return self.chain[-1]