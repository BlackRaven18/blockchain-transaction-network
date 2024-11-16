from clients.redis_client import RedisClient
import json

db_client = RedisClient.get_client()

def get_keys() -> list[str]:
    keys = db_client.get('keys')

    if keys is None:
        return []
    
    return json.loads(keys)

def add_key(key: str) -> str:
    print("Adding key...")
    print(key)

    keys = get_keys()

    if key in keys:
        return "Key already exists"
    
    keys.append(key)
    db_client.set('keys', json.dumps(keys))

    return "Key added"