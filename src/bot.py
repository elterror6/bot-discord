import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from dotenv import load_dotenv
import signal
import asyncio
import logging
from logger_config import get_logger
from salute_utils import init_salute_file

logger = get_logger("BOT")

logger = logging.getLogger("BOT")

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

def signal_handler(signal, frame):
    logger.info("Recibida señal de terminación. Desconectando...")
    loop = asyncio.get_event_loop()
    loop.create_task(shutdown_bot())

signal.signal(signal.SIGINT, signal_handler)

@bot.event
async def on_ready():
    
    logger.info(f"Conectado como {bot.user}")
    logger.info(f"Cargando datos ...")
    init_salute_file(bot)
    logger.info("Datos cargados correctamente.")

    logger.info("Cargando extensiones...")
    await cargar_extensiones()
    logger.info("Extensiones cargadas correctamente.")

    await registrar_comandos()


async def shutdown_bot():
    await limpiar_comandos()
    await bot.tree.sync(guild=None)  # Sincronización de comandos globales
    logger.info("Comandos globales actualizados correctamente.")
    logger.info("Desconectando...")
    await bot.close()

async def limpiar_comandos():
    try:
        logger.info("Limpiando comandos...")
        bot.tree.clear_commands(guild=None)
        await bot.tree.sync(guild=None)  # Limpieza de comandos
        logger.info("Comandos limpiados correctamente.")
    except Exception as e:
        logger.error(f"Error al limpiar comandos. Trace: {e}")

async def registrar_comandos():
    try:
        logger.info("Registrando comandos...")
        await bot.tree.sync()  # Registro de comandos
        logger.info(f"Comandos registrados correctamente. {len(bot.tree.get_commands())} comandos registrados.")
    except Exception as e:
        logger.error(f"Error al registrar comandos. Trace: {e}")
async def cargar_extensiones():
    await bot.load_extension("cogs.commands")
    await bot.load_extension("cogs.salute")

bot.run(TOKEN)