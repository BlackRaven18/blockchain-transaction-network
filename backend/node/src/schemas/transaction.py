from pydantic import BaseModel
from typing import Optional
import json

class Transaction(BaseModel):
    sender: str 
    recipient: str
    data: str
    signature: Optional[str] = None

    def serialize(self) -> str:
        return json.dumps(self.model_dump(exclude={"signature"}), sort_keys=True)