import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import logging
from logger_config import get_logger

load_dotenv()
logger = get_logger("DATABASE")
logger = logging.getLogger("DATABASE")


class Database:

    _instance = None

    def __init__ (self):
        mongo_uri = os.getenv("MONGO_URL")
        if not mongo_uri :
            logger.error("MONGO_URL no definido en el archivo .env")
            raise ValueError("MONGO_URL no definido en el archivo .env")
        self.client = AsyncIOMotorClient(mongo_uri)
        self.db = self.client["discord_bot"]
        logger.info("Conexión a la base de datos MongoDB establecida.")
        self.guilds = self.db["guild_config"]
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Database()
        return cls._instance
    
    async def test_connection (self):
        """"
        Prueba la conexión a la base de datos.
        """
        try:
            await self.client.admin.command('ping')
            logger.info("Conexión a la base de datos MongoDB exitosa.")
        except Exception as e:
            logger.error(f"Error al conectar a la base de datos MongoDB: {e}")