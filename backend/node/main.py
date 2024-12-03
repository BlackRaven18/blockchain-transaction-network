from fastapi import FastAPI
import uvicorn

from contextlib import asynccontextmanager

from routers import websocket
from routers import api

from clients.redis import RedisClient
from clients.logger import connect_to_logger, log

from config import init_config

from args import args
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_config()
    RedisClient.get_client()
    await connect_to_logger()
    await log("Hi there!")

    yield

    pass

app = FastAPI(lifespan=lifespan)
app.include_router(websocket.router)
app.include_router(api.router, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run("main:app", host=args.host, port=args.port, reload=True)

    
