import json

import websockets
import asyncio

from utils.utils import nodes, get_config

from schemas.transaction import Transaction

from repositories.blockchain_repository import get_blockchain, save_blockchain

from network.ConnectionsManager import ConnectionsManager, WebSocketClient

task = None

async def establish_websocket_connections():
    connections_manager = ConnectionsManager()
    for node in nodes:
        url = f"ws://{node.host}:{node.port}/ws"
        websocket_client = WebSocketClient(url)
        await websocket_client.connect()
        connections_manager.add_connection(websocket_client)

    print(connections_manager.web_socket_clients)

    return "network connections established"

async def verify_block():
    print("Verifying block...")
    return "accepted"

async def cancel_mine_block():
    global task

    if task is not None and not task.done():
        print("Cancelling block mining...")
        task.cancel()
        task = None
        print("Block mining cancelled")

    return "bebe2"

async def mine_block():
    global task

    blockchain = get_blockchain()
    new_block = blockchain.create_block()

    task = asyncio.create_task(new_block.mine_block(get_config()["mining_difficulty"]))
    task.add_done_callback(lambda task: save_blockchain(blockchain))

    task_result = await task

    if task_result is not None:
        response = await broadcast_action("cancel-and-verify-block", {})
        print("Block mining results: " + str(response))
    
    return "bebe"

async def check_if_should_mine_block():
    blockchain = get_blockchain()

    if blockchain.should_mine_block():
        await broadcast_action("mine-block", {})

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
    connection_manager = ConnectionsManager()

    payload = {"type": action, "data": data}

    # url_pool = [f"ws://{node.host}:{node.port}/ws" for node in nodes]
    # tasks = [send_action(url, payload) for url in url_pool]

    # results = await asyncio.gather(*tasks, return_exceptions=True)
    results = await connection_manager.send_to_all(json.dumps(payload))
    # results = "hmm..."

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