from pydantic import BaseModel

import datetime
import hashlib
import time
import asyncio

from schemas.transaction import Transaction

class Block(BaseModel):
    index: int
    timestamp: datetime.datetime = datetime.datetime.now()
    transactions: list[Transaction]
    nonce: int = 0
    hash: str
    previous_block_hash: str

    def model_post_init(self, __context):
        if self.index != 1:
            self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = self.model_dump_json().encode()
        return hashlib.sha256(block_string).hexdigest()
    
    async def mine_block(self, difficulty):
        target = '0' * difficulty
        start_time = time.time()

        while self.hash[:difficulty] != target:
            await asyncio.sleep(0)
            self.nonce += 1
            self.hash = self.calculate_hash()

        end_time = time.time()
        print(f"Block mined: {self.hash} (Nonce: {self.nonce})")
        print(f"Mining took {end_time - start_time:.4f} seconds\n")

        return self.model_dump_json()
