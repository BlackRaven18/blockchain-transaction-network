from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from contextlib import asynccontextmanager

from routers import websocket
from routers import api

from clients.redis import RedisClient
from clients.logger import connect_to_logger, log, MessageType

from config import init_config

from args import args
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_config()
    RedisClient.get_client()
    await connect_to_logger()
    await log(MessageType.STARTUP)

    yield

    await log(MessageType.DOWN)

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(websocket.router)
app.include_router(api.router, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run("main:app", host=args.host, port=args.port, reload=True)

    
