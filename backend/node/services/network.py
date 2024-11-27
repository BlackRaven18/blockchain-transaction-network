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

def cancel_mine_block():
    global task

    print("Cancelling block mining...")
    is_cancelled = task.cancel()

    if is_cancelled:
        print("Block mining cancelled")
    else:
        print("Block mining not cancelled")

    return "bebe2"

def mine_block():
    global task

    blockchain = get_blockchain()
    new_block = blockchain.create_block()

    task = asyncio.create_task(new_block.mine_block(get_config()["mining_difficulty"]))
    task.add_done_callback(lambda task_result_handler: asyncio.create_task(handle_mining_result(task)))

    return "Mining started"

async def handle_mining_result(task: asyncio.Task):
    """
    This function will be called once the mining task completes.
    """
    try:
        task_result = await task
        print("Task result: " + str(task_result))

        if task_result is not None and task.cancelled() is not True:
            print("I MINNED!!!!")
            response = await broadcast_action("cancel-and-verify-block", {}, receive_responses=False)
            print("Block mining results: " + str(response))
    except asyncio.CancelledError:
        print("Mining task was cancelled due to cancellation request.")
    except Exception as e:
        print(f"Error while processing mining result: {e}")

async def check_if_should_mine_block():
    blockchain = get_blockchain()

    if blockchain.should_mine_block():
        print("Should mine block...")
        await broadcast_action("mine-block", {}, receive_responses=False)

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


async def broadcast_action(action: str, data: dict[str, any], receive_responses = True):
    connection_manager = ConnectionsManager()
    results = ""
    payload = {"type": action, "data": data}

    if receive_responses:
        results = await connection_manager.send_and_receive_from_all(json.dumps(payload))
    else:
        await connection_manager.send_to_all(json.dumps(payload))

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