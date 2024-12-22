from fastapi import APIRouter, WebSocket, WebSocketDisconnect

import asyncio

from typing import List

router = APIRouter()

active_connections = []
consumers: List[WebSocket] = []

forward_delay_time = 2 # delay of network response

@router.websocket("/consume-logs")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            await asyncio.sleep(forward_delay_time)
            await notify_consumers(data)

    except WebSocketDisconnect:
        active_connections.remove(websocket)


@router.websocket("/register-consumer")
async def forward(websocket: WebSocket):
    await websocket.accept()

    consumers.append(websocket)
    print("---Consumer registered---")

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        consumers.remove(websocket)
        print("---Consumer disconnected---")


async def notify_consumers(message: str):
    for consumer in consumers:
        await send_message(consumer, message)


async def send_message(websocket: WebSocket, message: str):
    try:
        await websocket.send_text(message)
    except Exception as e:
        print(f"Error sending message: {e}")
