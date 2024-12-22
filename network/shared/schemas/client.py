from pydantic import BaseModel

class Client(BaseModel):
    id: str
    host: str
    port: int
    key: str
