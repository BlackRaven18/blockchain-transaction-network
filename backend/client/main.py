from fastapi import FastAPI
import uvicorn
import argparse
from routers import transactions
from routers import network
from args import args

app = FastAPI()
app.include_router(network.router, prefix="/api/v1")
app.include_router(transactions.router, prefix="/api/v1")

def main():
    uvicorn.run(
        "main:app",
        port=args.port,
        reload=args.reload
    )

if __name__ == "__main__":
    main()