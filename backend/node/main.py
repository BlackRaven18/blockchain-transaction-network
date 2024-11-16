from fastapi import FastAPI
import json
import uvicorn
import argparse
from schemas.blockchain import Blockchain
from schemas.node import Node
from routers import server_router_ws, server_router_api
from clients.http_client import get_network_structure

def get_network_peers(nodes: list[Node]):
    return [
        {
            "id": node.id, 
            "ws_url": f'ws://{node.host}:{node.port}', 
            "http_url": f'http://{node.host}:{node.port}'
        } for node in nodes
    ]

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
nodes: list[Node] = get_network_structure()
network_peers = get_network_peers(nodes)


app.include_router(server_router_ws.router)
app.include_router(server_router_api.router, prefix="/api/v1")

def main():

    uvicorn.run(
        "main:app",
        port=args.port,
        reload=True
    )

if __name__ == "__main__":
    main()