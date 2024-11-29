from pydantic import BaseModel

class PublicKey(BaseModel):
    owner: str
    key: str