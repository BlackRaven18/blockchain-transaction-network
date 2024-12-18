from fastapi import APIRouter
from services.network import start_logger, start_nodes, establish_connections
from utils.utils import get_config

router = APIRouter()
@router.post("/run-logger")
async def run_logger():
    start_logger()
    return {"message": "Logger started."}

@router.post("/start-network")
async def start_network():
    start_nodes()
    return {"message": "Network started."}

@router.post("/establish-network-connections")
async def establish_network_connections():
    await establish_connections()
    return {"message": "Network connections established."}

@router.get("/config")
async def get_network_config():
    config = get_config()
    return config
    
