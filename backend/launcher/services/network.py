import subprocess

import httpx
import asyncio

from utils.utils import get_config

running_processes = {}


def start_logger():
    
    run_command = f"uvicorn main:app --port {get_config()['logger_port']} --reload "
    start_terminal_command = f'start powershell -NoExit -Command "{run_command}"'

    try:
        subprocess.Popen(start_terminal_command, shell=True, cwd="../logger")
    except Exception as e:
        print(f"Error starting logger: {e}")


def start_nodes():
    for node in get_config()["nodes"]:
        run_command = f"python main.py --id {node['id']} --host {node['host']} --port {node['port']} --db_host {node['db']['host']} --db_port {node['db']['port']} --db_index {node['db']['index']}"

        start_terminal_command = f'start powershell -NoExit -Command "{run_command}"'
        print(start_terminal_command)

        try:
            subprocess.Popen(start_terminal_command, shell=True, cwd="../node")
        except Exception as e:
            print(f"Error starting node {node['id']}: {e}")


async def establish_connections():
    async with httpx.AsyncClient(timeout=10) as client:
        tasks = [
            client.post(
                f"http://{node['host']}:{node['port']}/api/v1/establish-connection",
                json={},
            )
            for node in get_config()["nodes"]
        ]

        responses = await asyncio.gather(*tasks)

        for response in responses:
            print(
                f"POST {response.request.url} -> {response.status_code}: {response.text}"
            )

        return responses
