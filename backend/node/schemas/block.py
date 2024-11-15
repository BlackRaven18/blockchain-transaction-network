from pydantic import BaseModel
import datetime
import hashlib
from schemas.transaction import Transaction


class Block(BaseModel):
    index: int
    timestamp: datetime.datetime = datetime.datetime.now()
    transactions: list[Transaction]
    hash: str
    previous_block_hash: str

    def model_post_init(self, __context):
        if self.index != 1:
            self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = self.model_dump_json().encode()
        return hashlib.sha256(block_string).hexdigest()
