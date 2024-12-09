import json

import websockets
from cryptography.hazmat.primitives import serialization

from services.cryptography import public_key

from schemas.client import Client

from args import args

async def share_public_key(server_url: str, server_port: int) -> str:
    print(f"Sending public key to ws://{server_url}:{server_port}/ws")

    try:
        async with websockets.connect(f"ws://{server_url}:{server_port}/ws") as websocket:

            client_public_key = Client(
                id=args.id,
                host=args.host,
                port=args.port, 
                key=public_key.public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.PKCS1).decode('utf-8')
            )

            ws_payload = {
                "type": "register-client",
                "data": client_public_key.model_dump_json(),
            }

            await websocket.send(json.dumps(ws_payload))

            response = await websocket.recv()
            print(response)

            return response
    except Exception as e:
        print(f"Could not send transaction to {server_url}:{server_port} - {e}")