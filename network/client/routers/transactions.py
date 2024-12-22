from fastapi import APIRouter, File, UploadFile, Form, HTTPException

import base64
from enum import Enum

from schemas.transaction import Transaction
from services.transaction import send_transaction
from args import args

router = APIRouter()

class PortOptions(int, Enum):
    port_8001 = 8001
    port_8002 = 8002
    port_8003 = 8003
    port_8004 = 8004
    port_8005 = 8005
    port_8006 = 8006

@router.post("/transactions/new")
async def new_transaction(
    server_url: str = Form("localhost"), 
    server_port: PortOptions = Form(PortOptions.port_8001),
    recipient_id: str = Form(), 
    file: UploadFile = File(None)
    ):

    if file is None:
        raise HTTPException(status_code=400, detail="No file uploaded.")
    
    file_content = await file.read()
    
    transaction = Transaction(sender=args.id, recipient=recipient_id, data=base64.b64encode(file_content).decode('utf-8'))
    print("Transaction: " + str(transaction.model_dump_json()))

    response = await send_transaction(server_url, server_port.value, transaction)

    return {"message": response}
