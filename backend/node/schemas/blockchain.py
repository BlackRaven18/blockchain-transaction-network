from typing import Any
from pydantic import BaseModel
from schemas.block import Block
from schemas.transaction import Transaction
from utils.utils import get_config

class Blockchain(BaseModel):
    chain: list[Block] = []
    current_transactions: list[Transaction] = []

    def model_post_init(self, __context: Any) -> None:
        if len(self.chain) == 0: 
            self.__create_genesis_block()

    def __create_genesis_block(self):
        print("Creating genesis block...")

        genesis_block = Block(
            index=0,
            hash="1",
            transactions=[],
            previous_block_hash="1"
        )

        self.add_block(genesis_block)

    def create_block(self) -> Block:

        block = Block(
            index=len(self.chain),
            hash="", # will be calculated during the mining process
            transactions=self.current_transactions,
            previous_block_hash=self.last_block.hash
        )

        return block

    def add_block(self, block: Block) -> None:
        self.current_transactions = []
        self.chain.append(block)
    
    def add_transaction(self, sender: str, recipient: str, data: str, signature: str) -> None:
        transaction = Transaction(
            sender=sender,
            recipient=recipient,
            data=data,
            signature=signature,
        )

        self.current_transactions.append(transaction)

    def should_mine_block(self) -> bool:
        return len(self.current_transactions) >= get_config()["max_block_size"]

    @property
    def last_block(self) -> Block:
        return self.chain[-1]