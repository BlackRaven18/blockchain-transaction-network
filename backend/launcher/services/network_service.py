import subprocess

import httpx
import asyncio

from utils.utils import get_config

running_processes = {}

def start_nodes():
    for node in get_config()["nodes"]:
        command = f"start powershell -NoExit -Command \"python main.py --id {node["id"]} --host {node["host"]} --port {node["port"]} --db_host {node["db"]["host"]} --db_port {node["db"]["port"]}\""
        print(command)
        try:
            subprocess.Popen(command, shell=True, cwd="../node")
        except Exception as e:
            print(f"Error starting node {node['id']}: {e}")

async def establish_connections():

    async with httpx.AsyncClient(timeout=10) as client:
        tasks = [
            client.post(f"http://{node['host']}:{node['port']}/api/v1/establish-connection", json={})
            for node in get_config()["nodes"]
        ]

        responses = await asyncio.gather(*tasks)

        for response in responses:
            print(f"POST {response.request.url} -> {response.status_code}: {response.text}")

        return responses
        # for node in get_config()["nodes"]:
        #     url = f"http://{node['host']}:{node['port']}/api/v1/establish-connection"
        #     response = client.post(url, json={})
        #     print(response.json())
