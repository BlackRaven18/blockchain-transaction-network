from fastapi import APIRouter

from repositories.blockchain import get_blockchain

from services.network import establish_websocket_connections

from repositories.public_key import get_public_keys

router = APIRouter()

@router.post("/establish-connection")
async def establish_connection():
    response = await establish_websocket_connections()
    return {"message": response}

@router.get("/chain")
async def get_chain():
    return {"blockchain": get_blockchain()}

@router.get("/current-transactions")
async def get_current_transactions():
    return {"transactions": get_blockchain().current_transactions}

@router.get("/clients")
async def get_clients():
    clients = get_public_keys()

    return {"clients": clients}