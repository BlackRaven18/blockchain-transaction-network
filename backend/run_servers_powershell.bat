@echo off

start powershell -NoExit -Command "python src/main.py --port 8000 --reload --id server1"

start powershell -NoExit -Command "python src/main.py --port 8001 --reload --id server2"

start powershell -NoExit -Command "python src/main.py --port 8002 --reload --id server3"
