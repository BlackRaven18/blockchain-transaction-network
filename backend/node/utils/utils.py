def get_args():
    from main import args
    return args

def get_db_data():
    from main import redis_client_data
    return redis_client_data

def get_blockchain():
    from main import blockchain
    return blockchain

def get_network_peers():
    from main import network_peers
    return network_peers

def get_network_ws_urls(endpoint: str):
    from main import network_peers
    print("Network peers: ", network_peers)
    return [peer['ws_url'] + endpoint for peer in network_peers]

def get_network_http_urls(endpoint: str):
    from main import network_peers
    return [peer['http_url'] + endpoint for peer in network_peers]