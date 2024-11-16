import json
from constants import CONFIG_PATH
from schemas.node import Node

config: dict = json.load(open(CONFIG_PATH, "r"))
nodes: list[Node] = [ Node(**peer) for peer in config ]