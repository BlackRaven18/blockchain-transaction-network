import json
from fastapi import FastAPI
import uvicorn
import argparse
from schemas.blockchain import Blockchain
from constants import CONFIG_PATH

def parse_args():
    parser = argparse.ArgumentParser(description="Run a FastAPI application with argparse")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to run the FastAPI app on")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the FastAPI app on")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload during development")
    parser.add_argument("--id", type=str, default="server0", help="ID of the peer")
    
    return parser.parse_args()

args = parse_args() 

app = FastAPI()
blockchain = Blockchain()
config = json.load(open(CONFIG_PATH, "r"))

network_peers = [
    {
        "id": peer["id"], 
        "ws_url": f'ws://{peer["host"]}:{peer["port"]}', 
        "http_url": f'http://{peer["host"]}:{peer["port"]}'
    } for peer in config
]

def main():
    uvicorn.run(
        "main:app",
        port=args.port,
        reload=args.reload
    )

if __name__ == "__main__":
    main()