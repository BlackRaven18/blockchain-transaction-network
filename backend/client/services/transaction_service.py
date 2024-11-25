import json

import websockets

from schemas.transaction import Transaction

from services.cryptography_service import sign_transaction

async def send_transaction(server_url: str, server_port: int, transaction: Transaction):

    transaction.signature = sign_transaction(transaction)
    Transaction.signature = transaction.signature

    print(f"Sending transaction to ws://{server_url}:{server_port}/ws")
    try:
        async with websockets.connect(f"ws://{server_url}:{server_port}/ws") as websocket:
            payload = {"type": "new-transaction-proposal", "data": transaction.model_dump_json()}
            await websocket.send(json.dumps(payload))
            response = await websocket.recv()
            print(response)
    except Exception as e:
        print(f"Could not send transaction to {server_url}:{server_port} - {e}")
