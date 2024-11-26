from fastapi import APIRouter, WebSocket, WebSocketDisconnect

import json
from typing import List

from schemas.transaction import Transaction

from repositories.keys_repository import add_public_key

from services.cryptography_service import verify_transaction
from services.network import broadcast_action, conduct_vote, save_transaction, check_if_should_mine_block, mine_block, cancel_mine_block, verify_block

router = APIRouter()

active_connections: List[WebSocket] = []

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            response = await handle_message(message)
            await websocket.send_text(response)
    except WebSocketDisconnect:
        active_connections.remove(websocket)

async def handle_message(message: str):
    """Handle incoming WebSocket messages."""
    try:
        data = json.loads(message)
        action = data.get("type")
        payload = data.get("data")

        response = None
        #-------------------------------------------------------------------------------
        # External actions (from clients)
        #-------------------------------------------------------------------------------
        if action == "new-transaction-proposal":

            transaction = Transaction(**json.loads(payload))
            result = await conduct_vote(transaction)

            response = result

            # await check_if_should_mine_block()

        elif action == "register-client":

            print("Adding public key...")
            print(payload)
            response = await broadcast_action("accept-client", payload)
        #-------------------------------------------------------------------------------
        # Internal actions (from other nodes)
        #-------------------------------------------------------------------------------
        elif action == "vote":

            transaction = Transaction(**json.loads(payload))
            result = verify_transaction(transaction)
            response = result

        elif action == "accept-transaction":
            transaction = Transaction(**json.loads(payload))
            response = save_transaction(transaction)

        elif action == "accept-client":

            response = add_public_key(payload)

        elif action == "mine-block":
            await mine_block()

            response = "Block mined"

        elif action == "cancel-and-verify-block":

            await cancel_mine_block()
            await verify_block()

            response = "Block mined and verified"


        elif action == "accept-block":

            pass

        else:
            print(f"Unknown action: {action}")

        print("Response: " + str(response))
        return response
    except json.JSONDecodeError:
        print("Invalid message format received.")