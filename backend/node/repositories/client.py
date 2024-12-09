import json

from clients.redis import RedisClient

from schemas.client import Client

db_client = RedisClient.get_client()

def get_clients() -> list[Client]:
    clients = db_client.get('clients')

    if clients is None:
        return []
    
    clients = [Client(**client) for client in json.loads(clients)]
    
    return clients

def get_client(client_id: str) -> Client | None:
    clients = get_clients()

    for client in clients:
        if client.id == client_id:
            return client

    return None

def add_client(client: Client) -> str:
    print("Adding client...")

    clients = get_clients()
    
    if client in clients:
        return "Client already exists"
    
    clients.append(client)
    db_client.set('clients', json.dumps([client.model_dump() for client in clients]))

    return "Client added"
