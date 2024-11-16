import httpx
from constants import LAUNCHER_URL
from schemas.node import Node

def get_network_structure() -> list[Node]:
    print("Getting network structure...")
    
    with httpx.Client() as client:
        response_raw = client.get(f"{LAUNCHER_URL}/nodes")
        response_json = response_raw.json()
        nodes: list[Node] = [ Node(**peer) for peer in response_json["nodes"] ]
        return nodes