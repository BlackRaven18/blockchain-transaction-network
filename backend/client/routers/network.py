from fastapi import APIRouter, Form

from enum import Enum

from services.network_service import share_public_key

router = APIRouter()

class PortOptions(int, Enum):
    port_8001 = 8001
    port_8002 = 8002
    port_8003 = 8003

@router.post("/connect")
async def connect(server_url: str = Form("localhost"), server_port: PortOptions = Form(PortOptions.port_8001)):
    response = await share_public_key(server_url, server_port.value)
    return {"message": response}
