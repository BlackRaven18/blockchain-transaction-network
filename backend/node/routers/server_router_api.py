from fastapi import APIRouter
from args import args
from repositories.blockchain_repository import get_blockchain

router = APIRouter()

@router.get("/chain")
async def get_chain():
    return {"blockchain": get_blockchain()}

@router.get("/current_transactions")
async def get_current_transactions():
    return {"transactions": get_blockchain().current_transactions}

@router.get("/id")
async def get_id():
    return {"id": args.id}
