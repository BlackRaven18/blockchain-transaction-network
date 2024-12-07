from fastapi import APIRouter, File, UploadFile, Form

from enum import Enum

from schemas.transaction import Transaction
from services.transaction import send_transaction
from args import args

router = APIRouter()

class PortOptions(int, Enum):
    port_8001 = 8001
    port_8002 = 8002
    port_8003 = 8003

@router.post("/transactions/new")
async def new_transaction(
    server_url: str = Form("localhost"), 
    server_port: PortOptions = Form(PortOptions.port_8001),
    recipient_id: str = Form(), 
    file: UploadFile = File(None)
    ):

    if file is None:
        return {"message": "No file uploaded."}
    
    transaction = Transaction(sender=args.id, recipient=recipient_id, data=file.filename)

    await send_transaction(server_url, server_port.value, transaction)

    return {"message": "Transaction proposal submitted."}
