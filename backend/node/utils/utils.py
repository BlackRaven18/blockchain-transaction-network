from clients.http_client import get_network_config
from schemas.node import Node
from args import args

# Encapsulated config object
config = {
    "config_data": None,
    "nodes": []
}

def get_network_ws_urls(endpoint: str):
    return [peer['ws_url'] + endpoint for peer in config["network_peers"]]

# def get_network_peers(nodes: list[Node]):
#     return [
#         {
#             "id": node.id,
#             "ws_url": f'ws://{node.host}:{node.port}',
#             "http_url": f'http://{node.host}:{node.port}'
#         } for node in nodes if node.id != args.id
#     ]

def get_config() -> dict:
    return config["config_data"]

def get_nodes() -> list[Node]:
    return config["nodes"]



def init_config():
    config_data = get_network_config()
    nodes = [Node(**node) for node in config_data["nodes"]]
    # network_peers = get_network_peers(nodes)

    # Store everything in the config object
    config["config_data"] = config_data
    config["nodes"] = nodes
    # config["network_peers"] = network_peers
