from fastapi import FastAPI
import json
import uvicorn
import argparse
from schemas.blockchain import Blockchain
from schemas.node import Node, Database
from routers import server_router_ws, server_router_api
from clients.http_client import get_network_structure
from clients.redis_client import RedisClient
from config import args

def get_network_peers(nodes: list[Node]):
    return [
        {
            "id": node.id, 
            "ws_url": f'ws://{node.host}:{node.port}', 
            "http_url": f'http://{node.host}:{node.port}'
        } for node in nodes
    ]

def get_db_data(nodes: list[Node]) -> Database:
    for node in nodes:
        if node.id == args.id:
            return node.db
    

app = FastAPI()
app.include_router(server_router_ws.router)
app.include_router(server_router_api.router, prefix="/api/v1")

nodes: list[Node] = get_network_structure()
network_peers = get_network_peers(nodes)

# Redis db init
redis_client_data = get_db_data(nodes)

RedisClient.get_client().set('blockchan', Blockchain().model_dump_json())

def main():

    print(args.port)
    
    uvicorn.run(
        "main:app",
        port=args.port,
        reload=True
    )

if __name__ == "__main__":
    main()