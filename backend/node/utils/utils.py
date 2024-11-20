def get_network_ws_urls(endpoint: str):
    from main import network_peers
    return [peer['ws_url'] + endpoint for peer in network_peers]

def get_config() -> dict:
    from main import config
    return config