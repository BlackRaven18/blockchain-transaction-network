import json

import websockets

from config import get_nodes

from network.ConnectionsManager import ConnectionsManager, WebSocketClient

mine_block_task = None

async def establish_websocket_connections():
    connections_manager = ConnectionsManager()
    for node in get_nodes():
        url = f"ws://{node.host}:{node.port}/ws"
        websocket_client = WebSocketClient(url)
        await websocket_client.connect()
        connections_manager.add_connection(websocket_client)

    print(connections_manager.web_socket_clients)

    return "network connections established"

async def broadcast_action(action: str, data: dict[str, any], receive_responses = True):
    connection_manager = ConnectionsManager()
    results = ""
    payload = {"type": action, "data": data}

    if receive_responses:
        results = await connection_manager.send_and_receive_from_all(json.dumps(payload))
    else:
        await connection_manager.send_to_all(json.dumps(payload))

    print("Broadcast results: " + str(results))

    return results

async def send_action(url, payload):
    try:
        async with websockets.connect(url) as websocket:
            await websocket.send(json.dumps(payload))
            response = await websocket.recv()
            return response
    except Exception as e:
        print(f"Could not send transaction to {url} - {e}")