import json

from clients.redis import RedisClient

from schemas.public_key import PublicKey

db_client = RedisClient.get_client()

def get_public_keys() -> list[PublicKey]:
    keys = db_client.get('keys')

    if keys is None:
        return []
    
    keys = [PublicKey(**key) for key in json.loads(keys)]
    
    return keys

def get_public_key(client_id: str) -> str | None:
    keys_data = get_public_keys()

    for key_data in keys_data:
        if key_data.owner == client_id:
            return key_data.key

    return None

#TODO: Add DTO dlass to represent key_data
def add_public_key(key_data: PublicKey) -> str:
    print("Adding key...")

    keys = get_public_keys()
    
    if key_data in keys:
        return "Key already exists"
    
    keys.append(key_data)
    db_client.set('keys', json.dumps([key.model_dump() for key in keys]))

    return "Key added"