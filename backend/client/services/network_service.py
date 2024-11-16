import websockets
import json
from cryptography.hazmat.primitives import serialization
from services.cryptography_service import public_key

async def share_public_key(server_url: str, server_port: int) -> str:
    print(f"Sending public key to ws://{server_url}:{server_port}/register-client")
    print(public_key)
    try:
        async with websockets.connect(f"ws://{server_url}:{server_port}/register-client") as websocket:
            key_data = {
                "id": "client",
                "public_key": public_key.public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.PKCS1).decode('utf-8')
            }
            await websocket.send(json.dumps(key_data))
            response = await websocket.recv()
            print(response)
            return response
    except Exception as e:
        print(f"Could not send transaction to {server_url}:{server_port} - {e}")