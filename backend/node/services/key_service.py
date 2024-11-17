
import asyncio
import websockets
from cryptography.hazmat.primitives import serialization
from utils.utils import get_network_ws_urls

async def broadcast_public_key(public_key: str) -> None:
    broadcast_pool = get_network_ws_urls("/register-public-key")

    tasks = [send_public_key(server, public_key) for server in broadcast_pool]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    print(results)

async def send_public_key(server: str, public_key: str) -> None:
    try:
        async with websockets.connect(server) as websocket:
            await websocket.send(public_key)
            response = await websocket.recv()
            return response
    except Exception as e:
        print(f"Could not send public key to {server}: {e}")
