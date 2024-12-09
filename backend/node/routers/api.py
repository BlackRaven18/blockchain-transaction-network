from fastapi import APIRouter

from repositories.blockchain import get_blockchain

from services.network import establish_websocket_connections

from repositories.client import get_clients

from error_flags import ErrorFlags

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
async def get_retistered_clients():
    clients = get_clients()

    return {"clients": clients}

@router.get("/health")
async def health_check():
    response = ErrorFlags().serialize()
    return {"message": response}

@router.post("/inject-node-damage-error")
async def inject_node_damage_error():
    response = await ErrorFlags().set_node_damage_error()

    return {"message": response}


@router.post("/reset-node-damage-error")
async def reset_node_damage_error():
    response = await ErrorFlags().reset_node_damage_error()

    return {"message": response}