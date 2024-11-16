from fastapi import APIRouter, File, UploadFile, Form
from enum import Enum
from schemas.transaction import Transaction
from services.transaction_service import send_transaction
from constants import CLIENT_ID

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
    
    transaction = Transaction(sender=CLIENT_ID, recipient=recipient_id, data=file.filename)

    # Send vote to other servers
    await send_transaction(server_url, server_port.value, transaction)

    return {"message": "Transaction proposal submitted."}
