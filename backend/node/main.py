from fastapi import FastAPI
import uvicorn
from schemas.node import Node
from routers import server_router_ws, server_router_api
from clients.http_client import get_network_config
from args import args

def get_network_peers(nodes: list[Node]):
    return [
        {
            "id": node.id, 
            "ws_url": f'ws://{node.host}:{node.port}', 
            "http_url": f'http://{node.host}:{node.port}'
        } for node in nodes # if node.id != args.id
    ]
    
app = FastAPI()
app.include_router(server_router_ws.router)
app.include_router(server_router_api.router, prefix="/api/v1")


config = get_network_config()
nodes: list[Node] = [Node(**node) for node in config["nodes"]]
network_peers = get_network_peers(nodes)

def main():
    pass

if __name__ == "__main__":
    uvicorn.run("main:app", host=args.host, port=args.port, reload=True)
    main()
