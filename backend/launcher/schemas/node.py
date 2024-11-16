from pydantic import BaseModel

class Database(BaseModel):
    host: str
    port: int

class Node(BaseModel):
    id: str
    host: str
    port: int
    db: Database
