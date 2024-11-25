from clients.http_client import get_network_config
from schemas.node import Node
from args import args

def get_network_ws_urls(endpoint: str):
    from main import network_peers
    return [peer['ws_url'] + endpoint for peer in network_peers]

def get_network_peers(nodes: list[Node]):
    return [
        {
            "id": node.id, 
            "ws_url": f'ws://{node.host}:{node.port}', 
            "http_url": f'http://{node.host}:{node.port}'
        } for node in nodes if node.id != args.id
    ]

def get_config() -> dict:
    return config

config = get_network_config()
nodes: list[Node] = [Node(**node) for node in config["nodes"]]
network_peers = get_network_peers(nodes)