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
    return {"result": response}

@router.post("/inject-node-damage-error")
async def inject_node_damage_error():
    response = await ErrorFlags().set_node_damage_error()

    return {"message": response}


@router.post("/reset-node-damage-error")
async def reset_node_damage_error():
    response = await ErrorFlags().reset_node_damage_error()

    return {"message": response}

@router.post("/inject-transaction-vote-error")
async def inject_transaction_vote_error():
    response = ErrorFlags().set_transaction_vote_error()

    return {"message": response}


@router.post("/reset-transaction-vote-error")
async def reset_transaction_vote_error():
    response = ErrorFlags().reset_transaction_vote_error()

    return {"message": response}


@router.post("/inject-block-mining-error")
async def inject_block_mining_error():
    response = ErrorFlags().set_block_mining_error()

    return {"message": response}


@router.post("/reset-block-mining-error")
async def reset_block_mining_error():
    response = ErrorFlags().reset_block_mining_error()

    return {"message": response}