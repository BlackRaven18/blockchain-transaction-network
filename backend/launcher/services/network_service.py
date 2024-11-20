import subprocess
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