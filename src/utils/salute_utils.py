"""
Utilidades para manejar saludos personalizados en un bot de Discord.
"""
import os
import json

DATA_FILE = "data/salute_data.json"
DEFAULT_SALUTE = "¡Hola! {user}"

def init_salute_file(bot):
    """
    Inicializa el archivo de datos de saludos si no existe.
    Agrega entradas para cada guild en las que el bot está presente.
    Args:
        bot (commands.Bot): La instancia del bot de Discord.
    """
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
    """
    Carga los datos de saludos desde el archivo JSON.
    Returns:
        dict: Un diccionario con los datos de saludos por guild.
    """
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)
def save_salute_data(data):
    """
    Guarda los datos de saludos en el archivo JSON.
    Args:
        data (dict): Un diccionario con los datos de saludos por guild.
    """
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
def add_guild_salute(guild_id, salute=DEFAULT_SALUTE, enabled=True):
    """
    Agrega o actualiza los datos de saludo para una guild específica.
    Args:
        guild_id (int): El ID de la guild.
        salute (str): El mensaje de saludo personalizado.
        enabled (bool): Indica si la funcionalidad de saludo está activada.
    """
    data = load_salute_data()
    data[str(guild_id)] = {
        "salute": salute,
        "enabled": enabled,
        "chanel_id": None
    }
    save_salute_data(data)