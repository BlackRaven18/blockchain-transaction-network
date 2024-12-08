from clients.launcher import get_network_config
from schemas.node import Node

config = {
    "config_data": [],
    "nodes": []
}

def get_network_ws_urls(endpoint: str):
    return [peer['ws_url'] + endpoint for peer in config["network_peers"]]

def get_config() -> dict:
    return config["config_data"]

def get_nodes() -> list[Node]:
    return config["nodes"]

def init_config():
    config_data = get_network_config()
    nodes = [Node(**node) for node in config_data["nodes"]]

    config["config_data"] = config_data
    config["nodes"] = nodes
