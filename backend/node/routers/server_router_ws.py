from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
from services.transaction_service import validate_transaction
from services.cryptography_service import verify_transaction
from schemas.transaction import Transaction
from config import args
from repositories.blockchain_repository import get_blockchain
from repositories.keys_repository import get_keys, add_key
from services.key_service import broadcast_public_key

router = APIRouter()

@router.websocket("/add-public-key")
async def add_public_key(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            public_key = await websocket.receive_text()
            response = add_key(public_key)
            await websocket.send_text(response)

    except WebSocketDisconnect:
        print("WebSocket connection closed")

@router.websocket("/register-client")
async def register_client(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            public_key = await websocket.receive_text()
            response = add_key(public_key)
            await broadcast_public_key(public_key)

            await websocket.send_text(response)

    except WebSocketDisconnect:
        print("WebSocket connection closed")

@router.websocket("/transaction/new")
async def new_transaction(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            transaction_string = await websocket.receive_text()
            transaction = Transaction(**json.loads(transaction_string))
            if verify_transaction(transaction):
                await websocket.send_text("Transaction is valid")
            else:
                await websocket.send_text("Transaction is invalid")

    except WebSocketDisconnect:
        print("WebSocket connection closed")

@router.websocket("/vote")
async def vote(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            transaction_string = await websocket.receive_text()
            transaction = json.loads(transaction_string)
            vote_result = validate_transaction(transaction['transaction'])
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
            blockchain = get_blockchain()
            transaction_string = await websocket.receive_text()
            transaction = Transaction(**json.loads(transaction_string))
            blockchain.add_transaction(transaction.sender, transaction.recipient, transaction.data)
            for transaction in blockchain.current_transactions:
                print(transaction.model_dump_json(indent=4))
            # print(json.dumps(blockchain.current_transactions))
            await websocket.send_text("Transaction added to the blockchain")

    except WebSocketDisconnect:
        print("WebSocket connection closed")