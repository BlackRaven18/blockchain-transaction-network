import json
import asyncio
import websockets
from schemas.transaction import Transaction
from utils.utils import get_network_ws_urls, get_config

async def conduct_vote(master_node_id: str,transaction: Transaction):
    print("Conducting vote...")
    votes_counter = 0

    vote_pool = get_network_ws_urls("/vote")
    vote_tasks = [get_vote(node_vote_url, transaction) for node_vote_url in vote_pool]

    print("Waiting for votes...")
    votes = await asyncio.gather(*vote_tasks, return_exceptions=True)

    print("Counting votes...")
    for vote in votes:
        vote = json.loads(vote)
        if vote['vote'] is True:
            votes_counter += 1

    if votes_counter >= get_config()["min_approvals_to_accept_transaction"]:
        await broadcast_transaction(transaction)
        return("Transaction approved, broadcasting to other nodes")
    
    return("Transaction rejected")

async def broadcast_transaction(transaction: Transaction):
    print("Broadcasting transaction...")
    transaction_pool = get_network_ws_urls("/accept_transaction")
    send_transaction_tasks = [send_transaction(node_accept_transaction_url, transaction) for node_accept_transaction_url in transaction_pool]

    await asyncio.gather(*send_transaction_tasks, return_exceptions=True)

async def get_vote(node_vote_url, transaction: Transaction):
    print("Getting vote...")
    try:
        async with websockets.connect(node_vote_url) as websocket:
            await websocket.send(transaction.model_dump_json())
            vote_response = await websocket.recv()
            return vote_response
    except Exception as e:
        print(f"Could not send vote to {node_vote_url}: {e}")
        return None 


async def send_transaction(node_accept_transaction_url: str, transaction: Transaction):
    try:
        async with websockets.connect(node_accept_transaction_url) as websocket:
            transaction_json = transaction.model_dump_json()
            await websocket.send(transaction_json)
            response = await websocket.recv()
            print(response)
    except Exception as e:
        print(f"Could not send transaction to {node_accept_transaction_url}: {e}")