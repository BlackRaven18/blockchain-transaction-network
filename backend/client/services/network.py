import websockets
import json
from cryptography.hazmat.primitives import serialization
from services.cryptography import public_key
from args import args

async def share_public_key(server_url: str, server_port: int) -> str:
    print(f"Sending public key to ws://{server_url}:{server_port}/ws")
    print(public_key)
    try:
        async with websockets.connect(f"ws://{server_url}:{server_port}/ws") as websocket:
            key_data = {
                "id": args.id,
                "public_key": public_key.public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.PKCS1).decode('utf-8')
            }

            ws_payload = {
                "type": "register-client",
                "data": key_data
            }
            await websocket.send(json.dumps(ws_payload))
            response = await websocket.recv()
            print(response)
            return response
    except Exception as e:
        print(f"Could not send transaction to {server_url}:{server_port} - {e}")