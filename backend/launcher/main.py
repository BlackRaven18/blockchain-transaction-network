from fastapi import FastAPI

from routers import network

app = FastAPI()
app.include_router(network.router, prefix="/api/v1")