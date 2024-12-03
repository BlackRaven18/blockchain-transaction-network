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
    }

logger: WebSocketClient

async def connect_to_logger():
    global logger

    logger = WebSocketClient(f"ws://localhost:{config['config_data']['logger_port']}/consume-logs")

    await logger.connect()
    print("Connected to logger")

async def log(message: MessageType):
    await logger.send(json.dumps(message.value))
