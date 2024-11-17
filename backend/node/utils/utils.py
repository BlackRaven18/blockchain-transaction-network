def get_network_ws_urls(endpoint: str):
    from main import network_peers
    return [peer['ws_url'] + endpoint for peer in network_peers]