from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
from services.transaction_service import validate_transaction
from schemas.transaction import Transaction
from utils.utils import get_args, get_blockchain

router = APIRouter()


@router.websocket("/vote")
async def vote(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            args = get_args()
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