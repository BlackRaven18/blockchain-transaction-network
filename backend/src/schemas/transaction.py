from pydantic import BaseModel

class Transaction(BaseModel):
    sender: str 
    recipient: str
    data: str