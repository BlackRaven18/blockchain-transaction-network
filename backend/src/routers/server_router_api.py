from fastapi import APIRouter, File, UploadFile, Form
from schemas.transaction import Transaction
from services.transaction_service import broadcast_vote
from utils.utils import get_args, get_blockchain

router = APIRouter()

@router.post("/transactions/new")
async def new_transaction(sender: str = Form(), recipient: str = Form(), file: UploadFile = File(None)):
    transaction = Transaction(sender=sender, recipient=recipient, data=file.filename)

    # Send vote to other servers
    await broadcast_vote(transaction)

    return {"message": "Transaction proposal submitted."}

@router.get("/chain")
async def get_chain():
    return {"length": len(get_blockchain().chain), "chain": get_blockchain().chain}

@router.get("/current_transactions")
async def get_current_transactions():
    return {"transactions": get_blockchain().current_transactions}

@router.get("/id")
async def get_id():
    return {"id": get_args().id}
