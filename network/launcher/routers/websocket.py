from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from utils.utils import get_config

from services.network import establish_connections

router = APIRouter()

ready_nodes = []

@router.websocket("/ws/register-ready-node")
async def register_ready_node(websocket: WebSocket):
    global ready_nodes

    await websocket.accept()

    try:
        while True:
            message = await websocket.receive_text()
            print("Message received: " + message)

            if message not in ready_nodes:
                ready_nodes.append(message)

            print(f"Ready nodes: {ready_nodes}")

            if len(ready_nodes) == len(get_config()["nodes"]):
                print("All nodes are ready, establishing connections between nodes...")

                await establish_connections()

                ready_nodes = []
                print("Connections established")

    except WebSocketDisconnect:
        print("WebSocket connection closed")



