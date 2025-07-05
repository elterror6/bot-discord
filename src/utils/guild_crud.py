from database import Database

db = Database.get_instance()

collection = db.guilds

#CREATE
async def add_guild(guild_id: str, data: dict):
    """
    Agrega los datos de configuración de una guild en la base de datos.
    
    Args:
        guild_id (str): El ID de la guild.
        data (dict): Un diccionario con los datos de configuración de la guild.
    """
    await collection.update_one({"_id": guild_id}, {"$set": data}, upsert=True)
#READ
async def get_guild(guild_id: str):
    """
    Obtiene los datos de configuración de una guild desde la base de datos.
    
    Args:
        guild_id (str): El ID de la guild.
    
    Returns:
        dict: Un diccionario con los datos de configuración de la guild, o None si no existe.
    """
    guild_data = await collection.find_one({"_id": guild_id})
    return guild_data if guild_data else None
#UPDATE
async def update_guild(guild_id: str, key: str, value):
    """
    Actualiza un campo específico de los datos de configuración de una guild en la base de datos.
    
    Args:
        guild_id (str): El ID de la guild.
        key (str): La clave del campo a actualizar.
        data (dict): Un diccionario con los nuevos datos para el campo especificado.
    """
    await collection.update_one({"_id": guild_id}, {"$set": {key: value}})
#DELETE
async def delete_guild(guild_id: str):
    """
    Elimina los datos de configuración de una guild de la base de datos.
    
    Args:
        guild_id (str): El ID de la guild.
    """
    await collection.delete_one({"_id": guild_id})