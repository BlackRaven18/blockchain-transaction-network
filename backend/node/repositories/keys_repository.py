from clients.redis_client import RedisClient
import json

db_client = RedisClient.get_client()

def get_public_keys() -> list[dict[str, any]]:
    keys = db_client.get('keys')

    if keys is None:
        return []
    
    return json.loads(keys)

def get_public_key(client_id: str) -> str | None:
    keys = get_public_keys()

    for key in keys:
        key = json.loads(key)
        print("Key is")
        print(key)
        if key['id'] == client_id:
            return key['public_key']

    return None

#TODO: Add DTO dlass to represent key_data
def add_public_key(key_data: dict[str, any]) -> str:
    print("Adding key...")
    print(key_data)

    keys = get_public_keys()


    if key_data in keys:
        return "Key already exists"
    
    keys.append(key_data)
    db_client.set('keys', json.dumps(keys))

    return "Key added"