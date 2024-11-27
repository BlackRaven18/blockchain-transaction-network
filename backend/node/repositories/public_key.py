import json

from clients.redis import RedisClient

db_client = RedisClient.get_client()

def get_public_keys() -> list[dict[str, any]]:
    keys = db_client.get('keys')

    if keys is None:
        return []
    
    return json.loads(keys)

def get_public_key(client_id: str) -> str | None:
    keys_data = get_public_keys()

    for key_data in keys_data:
        if key_data['id'] == client_id:
            return key_data['public_key']

    return None

#TODO: Add DTO dlass to represent key_data
def add_public_key(key_data: dict[str, any]) -> str:
    print("Adding key...")

    keys = get_public_keys()
    
    if key_data in keys:
        return "Key already exists"
    
    keys.append(key_data)
    db_client.set('keys', json.dumps(keys))

    return "Key added"