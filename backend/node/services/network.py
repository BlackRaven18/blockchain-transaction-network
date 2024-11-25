import json

import websockets
import asyncio

from utils.utils import nodes, get_config

from schemas.transaction import Transaction

from repositories.blockchain_repository import get_blockchain, save_blockchain

def save_transaction(transaction: Transaction):
    blockchain = get_blockchain()
    blockchain.add_transaction(transaction.sender, transaction.recipient, transaction.data, transaction.signature)
    save_blockchain(blockchain)

    return "Transaction added to the blockchain"

async def conduct_vote(transaction: Transaction):
    print("Conducting vote...")
    votes_counter = 0

    votes = await broadcast_action("vote", transaction.model_dump_json())

    print("Vote results: " + str(votes))

    print("Counting votes...")
    for vote in votes:
        if vote == "valid":
            votes_counter += 1

    if votes_counter >= get_config()["min_approvals_to_accept_transaction"]:
        return await broadcast_action("accept-transaction", transaction.model_dump_json())
    
    return "Transaction rejected"


async def broadcast_action(action: str, data: dict[str, any]):
    payload = {"type": action, "data": data}

    url_pool = [f"ws://{node.host}:{node.port}/ws" for node in nodes]
    tasks = [send_action(url, payload) for url in url_pool]

    results = await asyncio.gather(*tasks, return_exceptions=True)
    print("Broadcast results: " + str(results))

    return results

async def send_action(url, payload):
    try:
        async with websockets.connect(url) as websocket:
            await websocket.send(json.dumps(payload))
            response = await websocket.recv()
            return response
    except Exception as e:
        print(f"Could not send transaction to {url} - {e}")