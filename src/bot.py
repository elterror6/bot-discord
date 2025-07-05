"""
Este archivo es el punto de entrada del bot de Discord.
"""
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from dotenv import load_dotenv
import signal
import asyncio
import logging
from logger_config import get_logger
from utils.image_utils import generate_default_welcome_image
from utils.database import Database
from utils.guild_crud import add_guild, get_guild, update_guild, delete_guild, ensure_all_guilds

logger = get_logger("BOT")

logger = logging.getLogger("BOT")

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

def signal_handler(signal, frame):
    """"
    Maneja la señal de terminación del bot (Ctrl + C).
    """
    logger.info("Recibida señal de terminación. Desconectando...")
    loop = asyncio.get_event_loop()
    loop.create_task(shutdown_bot())

signal.signal(signal.SIGINT, signal_handler)

@bot.event
async def on_ready():
    """
    Evento que se ejecuta cuando el bot se conecta a Discord.
    Registra los comandos y carga las extensiones.
    También inicializa el archivo de saludos y registra los comandos globales.
    """
    db = Database.get_instance()
    await db.test_connection()

    logger.info(f"Conectado como {bot.user}")
    logger.info(f"Comprobando datos ...")
    await ensure_all_guilds(bot)  # Asegura que todas las guilds tengan su configuración inicial
    logger.info("Datos verificados correctamente.")

    logger.info("Cargando extensiones...")
    try:
        await cargar_extensiones()
    except Exception as e:
        logger.error(f"Error al cargar extensiones. Trace: {e}")
    logger.info("Extensiones cargadas correctamente.")

    await registrar_comandos()


async def shutdown_bot():
    """
    Cierra el bot de Discord y limpia los comandos.
    """
    await limpiar_comandos()
    await bot.tree.sync(guild=None)  # Sincronización de comandos globales
    logger.info("Comandos globales actualizados correctamente.")
    logger.info("Desconectando...")
    await bot.close()

async def limpiar_comandos():
    """
    Limpia los comandos del bot.
    Esto es útil para evitar conflictos con comandos antiguos.
    """
    try:
        logger.info("Limpiando comandos...")
        bot.tree.clear_commands(guild=None)
        await bot.tree.sync(guild=None)  # Limpieza de comandos
        logger.info("Comandos limpiados correctamente.")
    except Exception as e:
        logger.error(f"Error al limpiar comandos. Trace: {e}")

async def registrar_comandos():
    """
    Registra los comandos del bot.
    Esto se hace al iniciar el bot y también al cargar las extensiones.
    """
    try:
        logger.info("Registrando comandos...")
        await bot.tree.sync()  # Registro de comandos
        logger.info(f"Comandos registrados correctamente. {len(bot.tree.get_commands())} comandos registrados.")
    except Exception as e:
        logger.error(f"Error al registrar comandos. Trace: {e}")

async def cargar_extensiones():
    """
    Carga las extensiones del bot.
    Las extensiones son módulos que contienen comandos y eventos del bot.
    """
    await bot.load_extension("cogs.commands")
    await bot.load_extension("cogs.salute")

@bot.event
async def on_guild_join(guild):
    """
    Evento que se ejecuta cuando el bot se une a un nuevo servidor.
    Registra el servidor y crea un saludo predeterminado.
    """
    logger.info(f"Unido al servidor: {guild.name} (ID: {guild.id})")
    add_guild(guild.id)
@bot.event
async def on_guild_remove(guild):
    """
    Evento que se ejecuta cuando el bot es eliminado de un servidor.
    Elimina los datos de saludo del servidor.
    """
    logger.info(f"Desconectado del servidor: {guild.name} (ID: {guild.id})")
    data = get_guild(guild_id=str(guild.id))
    if str(guild.id) in data:
        await delete_guild(guild_id=str(guild.id))
    logger.info(f"Datos de saludo eliminados para el servidor: {guild.name} (ID: {guild.id})")

@bot.event
async def on_member_join(member):
    """
    Evento que se ejecuta cuando un nuevo miembro se une a un servidor.
    Envía un mensaje de saludo al canal de texto predeterminado del servidor.
    """
    gui = str(member.guild.id)
    data = get_guild(guild_id=gui)
    
    if not data.get(gui, {}).get("enabled", False):
        return
    
    msg_template = data[gui].get("salute", "¡Hola! {user}!")
    msg = msg_template.format(user=member.mention)

    for channel in member.guild.text_channels:
        if channel.permissions_for(member.guild.me).send_messages:
            file = generate_default_welcome_image(member)
            await channel.send(content=msg, file=file)
            break

bot.run(TOKEN)