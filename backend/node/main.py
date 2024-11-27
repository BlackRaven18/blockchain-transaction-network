from fastapi import FastAPI

from contextlib import asynccontextmanager

import uvicorn

from routers import server_router_ws, server_router_api

from clients.redis_client import RedisClient

from utils.utils import init_config

from args import args
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_config()
    RedisClient.get_client()

    yield

    pass

app = FastAPI(lifespan=lifespan)
app.include_router(server_router_ws.router)
app.include_router(server_router_api.router, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run("main:app", host=args.host, port=args.port, reload=True)

    
