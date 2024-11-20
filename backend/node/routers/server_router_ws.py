from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
from services.cryptography_service import verify_transaction
from schemas.transaction import Transaction
from args import args
from repositories.blockchain_repository import get_blockchain, save_blockchain
from repositories.keys_repository import add_public_key
from services.key_service import broadcast_public_key
from services.transaction_service import conduct_vote, broadcast_transaction

router = APIRouter()

@router.websocket("/register-public-key")
async def register_public_key(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            public_key_data_raw = await websocket.receive_text()
            public_key: dict[str, any] = json.loads(public_key_data_raw)        # { id, public_key }
            response = add_public_key(public_key)
            
            await websocket.send_text(response)

    except WebSocketDisconnect:
        print("WebSocket connection closed")

@router.websocket("/register-client")
async def register_client(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            public_key = await websocket.receive_text()
            response = await broadcast_public_key(public_key)

            print("Client registered")

            await websocket.send_text("Client registered")

    except WebSocketDisconnect:
        print("WebSocket connection closed")

@router.websocket("/transaction/new")
async def new_transaction(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            print("Received new transaction...")
            transaction_string = await websocket.receive_text()
            transaction = Transaction(**json.loads(transaction_string))

            is_transaction_accepted = await conduct_vote(transaction)
            
            if is_transaction_accepted is True:
                await broadcast_transaction(transaction)
                await websocket.send_text("Transaction accepted")
            else:
                await websocket.send_text("Transaction rejected")

    except WebSocketDisconnect:
        print("WebSocket connection closed")

@router.websocket("/vote")
async def vote(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            transaction_string = await websocket.receive_text()
            transaction = Transaction(**json.loads(transaction_string))
            vote_result = verify_transaction(transaction)

            print("Server " + args.id + " voted: " + str(vote_result))

            vote_data = {
                'server_id': args.id,
                'vote': vote_result,
                'transaction': json.loads(transaction_string)
            }
            vote_data_json = json.dumps(vote_data)
            await websocket.send_text(vote_data_json)

    except WebSocketDisconnect:
        print("WebSocket connection closed")

@router.websocket("/accept_transaction")
async def accept_transaction(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            print("Adding transaction to blockchain...")
            blockchain = get_blockchain()
            transaction_raw= await websocket.receive_text()
            transaction = Transaction(**json.loads(transaction_raw))
            blockchain.add_transaction(transaction.sender, transaction.recipient, transaction.data, transaction.signature)
            save_blockchain(blockchain)

            for transaction in blockchain.current_transactions:
                print(transaction.model_dump_json(indent=4))

            await websocket.send_text("Transaction added to the blockchain")

    except WebSocketDisconnect:
        print("WebSocket connection closed")