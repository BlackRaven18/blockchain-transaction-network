from fastapi import APIRouter
from services.network_service import start_nodes, get_nodes
from schemas.node import Node

router = APIRouter()

@router.post("/start_network")
async def start_network():
    start_nodes()
    return {"message": "Network started."}

@router.get("/nodes")
async def get_network_structure():
    nodes: list[Node] = get_nodes()
    return {"nodes": nodes}
    
