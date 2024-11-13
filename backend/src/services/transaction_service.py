import json
import asyncio
import websockets
from schemas.transaction import Transaction
from utils.utils import get_args, get_network_ws_urls

async def broadcast_vote(transaction: Transaction):
    votes = []
    vote_data = {
        "server_id": get_args().id,
        "transaction": transaction.model_dump(),
    }
    vote_counter = 0
    vote_data_json = json.dumps(vote_data)

    vote_pool = get_network_ws_urls("/vote")

    vote_tasks = [send_vote(server, vote_data_json) for server in vote_pool]
    results = await asyncio.gather(*vote_tasks, return_exceptions=True)
    
    # Process responses
    vote_counter = 0
    for result in results:
        if isinstance(result, dict) and result.get('vote') is True:
            vote_counter += 1
            votes.append(result)

    for vote in votes:
        if vote['vote'] is True:
            vote_counter += 1

    if vote_counter >= 2:
        print("Vote approved")

        accept_transaction_pool = get_network_ws_urls("/accept_transaction")

        send_transaction_tasks = [send_transaction(server, transaction) for server in accept_transaction_pool]
        send_transactions_results = await asyncio.gather(*send_transaction_tasks, return_exceptions=True)

        for result in send_transactions_results:
            print(result)

    else:
        print("Vote rejected")

async def send_vote(server: str, vote_data_json: str):
    try:
        async with websockets.connect(server) as websocket:
            await websocket.send(vote_data_json)
            vote_response = json.loads(await websocket.recv())
            return vote_response
    except Exception as e:
        print(f"Could not send vote to {server}: {e}")
        return None 
    
async def send_transaction(server: str, transaction: Transaction):
    try:
        async with websockets.connect(server) as websocket:
            transaction_json = transaction.model_dump_json()
            await websocket.send(transaction_json)
            response = await websocket.recv()
            print(response)
    except Exception as e:
        print(f"Could not send transaction to {server}: {e}")

def validate_transaction(transaction) -> bool:
    return True  