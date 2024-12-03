from fastapi import APIRouter, WebSocket, WebSocketDisconnect

import json
from typing import List

from schemas.public_key import PublicKey
from schemas.transaction import Transaction
from schemas.block import Block

from repositories.public_key import add_public_key

from services.cryptography import verify_transaction
from services.blockchain import conduct_vote, save_transaction, save_block, check_if_should_mine_block, mine_block, cancel_mine_block, verify_block
from services.network import broadcast_action

from clients.logger import log

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

            if response is not None:
                await websocket.send_text(response)
    except WebSocketDisconnect:
        active_connections.remove(websocket)

async def handle_message(message: str):
    """Handle incoming WebSocket messages."""
    try:
        data = json.loads(message)
        action = data.get("type")
        payload = data.get("data")

        """ 
        response is a message that will be send to the client via websocket, 
        so if user don't read it, it will remain in websocket queue.
        response should be created only if user will read it!
        """

        response = None
        #-------------------------------------------------------------------------------
        # External actions (from clients)
        #-------------------------------------------------------------------------------
        if action == "new-transaction-proposal":

            transaction = Transaction(**json.loads(payload))
            result = await conduct_vote(transaction)

            response = result

            await check_if_should_mine_block()

        elif action == "register-client":

            print("Adding public key...")
            print(payload)
            response = await broadcast_action("accept-client", payload)
            await log('client-registered')
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
            public_key = PublicKey(**json.loads(payload))
            response = add_public_key(public_key)
            await log('client-registered')
            
        elif action == "mine-block":
            mine_block()

        elif action == "cancel-and-verify-block":
            cancel_mine_block()
            response = verify_block(Block(**json.loads(payload)))

        elif action == "accept-block":
            save_block(Block(**json.loads(payload)))
            print("Block added to the blockchain")

        else:
            print(f"Unknown action: {action}")

        print("Response: " + str(response))
        return response
    except json.JSONDecodeError:
        print("Invalid message format received.")