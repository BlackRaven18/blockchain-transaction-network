from enum import Enum
import json

from config import config
from args import args

from network.WebSocketClient import WebSocketClient

class MessageType(Enum):
    STARTUP = {
        "source": args.id,
        "status": "idle"
    },
    IDLE = {
        "source": args.id,
        "status": "idle"
    },
    CONDUCTING_VOTE = {
        "source": args.id,
        "status": "conducting-vote"
    },
    VOTING = {
        "source": args.id,
        "status": "voting"
    },
    MINING = {
        "source": args.id,
        "status": "mining"
    },
    VERIFING_BLOCK = {
        "source": args.id,
        "status": "verifying-block"
    },
    SAVING_TRANSACTION = {
        "source": args.id,
        "status": "saving-transaction"
    },
    SAVING_BLOCK = {
        "source": args.id,
        "status": "saving-block"
    },
    ADDING_CLIENT = {
        "source": args.id,
        "status": "adding-client"
    },

logger: WebSocketClient
log_queue = []

async def connect_to_logger():
    global logger

    logger = WebSocketClient(f"ws://localhost:{config['config_data']['logger_port']}/consume-logs")

    await logger.connect()
    print("Connected to logger")



async def log(message: MessageType):
    global log_queue
    
    log_queue.append(message.value)

    await logger.send(json.dumps(log_queue.pop(0)))
