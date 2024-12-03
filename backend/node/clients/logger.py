import json

from config import config
from args import args

from network.WebSocketClient import WebSocketClient

logger: WebSocketClient

async def connect_to_logger():
    global logger

    logger = WebSocketClient(f"ws://localhost:{config['config_data']['logger_port']}/consume-logs")

    await logger.connect()
    print("Connected to logger")

async def log(message: str):

    custom_message = {
        "source": args.id,
        "message": message
    }

    await logger.send(json.dumps(custom_message))
