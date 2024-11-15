from fastapi import FastAPI
import uvicorn
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Run a FastAPI application with argparse")
    parser.add_argument("--host", type=str, default="localhost", help="Host to run the FastAPI app on")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the FastAPI app on")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload during development")
    parser.add_argument("--id", type=str, default="client0", help="ID of the peer")
    
    return parser.parse_args()

args = parse_args() 

app = FastAPI()

def main():
    uvicorn.run(
        "main:app",
        port=args.port,
        reload=args.reload
    )

if __name__ == "__main__":
    main()