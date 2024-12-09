import json
from constants import CONFIG_PATH

def get_config() -> dict:
    config = json.load(open(CONFIG_PATH, "r"))
    return config