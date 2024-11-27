import httpx
from constants import LAUNCHER_URL
    
def get_network_config ()-> dict[str, any]:
    print("Getting network config...")
    
    with httpx.Client() as client:
        response_raw = client.get(f"{LAUNCHER_URL}/config")
        response_json = response_raw.json()
        return response_json