import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Run a FastAPI application with argparse")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to run the FastAPI app on")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the FastAPI app on")
    parser.add_argument("--db_host", type=str, default="127.0.0.1", help="Host to run the FastAPI app on")
    parser.add_argument("--db_port", type=int, default=63791, help="Port to run the FastAPI app on")
    parser.add_argument("--id", type=str, default="server0", help="ID of the peer")
    
    return parser.parse_args()

args = parse_args() 
