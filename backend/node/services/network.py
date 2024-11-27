import json

import websockets
import asyncio

from utils.utils import get_config, get_nodes

from schemas.transaction import Transaction
from schemas.block import Block

from repositories.blockchain_repository import get_blockchain, save_blockchain

from network.ConnectionsManager import ConnectionsManager, WebSocketClient

mine_block_task = None

async def establish_websocket_connections():
    connections_manager = ConnectionsManager()
    for node in get_nodes():
        url = f"ws://{node.host}:{node.port}/ws"
        websocket_client = WebSocketClient(url)
        await websocket_client.connect()
        connections_manager.add_connection(websocket_client)

    print(connections_manager.web_socket_clients)

    return "network connections established"

def verify_block(mined_block: Block):
    print("Verifying block...")
    blockchain = get_blockchain()
    last_block = blockchain.last_block

    if mined_block.previous_block_hash != last_block.hash:
        print("Block does not have correct previous hash.")
        return "rejected"

    if mined_block.hash != mined_block.calculate_hash():
        print("Block hash is not correct.")
        return "rejected"
    
    return "accepted"

def cancel_mine_block():
    global mine_block_task

    print("Cancelling block mining...")
    is_cancelled = mine_block_task.cancel()

    if is_cancelled:
        response = "Block mining cancelled"
    else:
        response = "Block mining not cancelled"

    return response

def mine_block():
    global mine_block_task

    blockchain = get_blockchain()
    new_block = blockchain.create_block()

    mine_block_task = asyncio.create_task(new_block.mine_block(get_config()["mining_difficulty"]))
    mine_block_task.add_done_callback(lambda task_result_handler: asyncio.create_task(handle_mining_result(mine_block_task)))

    return "Mining started"

async def handle_mining_result(mine_block_task: asyncio.Task):
    """
    This function will be called once the mining task completes.
    """
    try:
        mined_block = await mine_block_task
        print("Minned block: " + str(mined_block.model_dump_json()))

        if mined_block is not None and mine_block_task.cancelled() is not True:
            print("I mined a block!!!!")
            responses = await broadcast_action("cancel-and-verify-block", mined_block.model_dump_json())

            print("Block mining results: " + str(responses))
            for response in responses:
                if response == "rejected":
                    print("One of the nodes rejected the block.")
                    return
            await broadcast_action("accept-block", mined_block.model_dump_json(), receive_responses=False)

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

def save_block(block: Block):
    blockchain = get_blockchain()
    blockchain.add_block(block)
    save_blockchain(blockchain)

    return "Block added to the blockchain"

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