import httpx
import websockets

from args import args

from constants import LAUNCHER_API_URL, LAUNCHER_WS_URL
    
def get_network_config () -> dict[str, any]:
    print("Getting network config...")
    
    with httpx.Client() as client:
        response_raw = client.get(f"{LAUNCHER_API_URL}/config")
        response_json = response_raw.json()
        return response_json
    
async def confirm_readiness() -> None:

    try:
        async with websockets.connect(f"{LAUNCHER_WS_URL}/ws/register-ready-node") as websocket:
            await websocket.send(f"{args.id} ready" )

            print("Readiness confirmed")

    except Exception as e:
        print(f"Error confirming readiness: {e}")