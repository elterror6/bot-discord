import os
import json

DATA_FILE = "data/salute_data.json"
DEFAULT_SALUTE = "¡Hola! {user}"

def init_salute_file(bot):

    if not os.path.exists(DATA_FILE):
        data = {}
    else:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    updated = False
    for guild in bot.guilds:
        gid = str(guild.id)
        if gid not in data:
            data[gid] = {
                "salute": DEFAULT_SALUTE,
                "enabled": False,
                "chanel_id": None
            }
            updated = True
    if updated:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

def load_salute_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)
def save_salute_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
def add_guild_salute(guild_id, salute=DEFAULT_SALUTE, enabled=True):
    data = load_salute_data()
    data[str(guild_id)] = {
        "salute": salute,
        "enabled": enabled,
        "chanel_id": None
    }
    save_salute_data(data)