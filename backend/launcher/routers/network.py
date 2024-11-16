from fastapi import APIRouter
from services.network_service import start_nodes

router = APIRouter()

@router.post("/start_network")
async def start_network():
    start_nodes()
    return {"message": "Network started."}
    
