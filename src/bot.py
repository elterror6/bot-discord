import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from dotenv import load_dotenv
import signal
import asyncio

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

def signal_handler(signal, frame):
    print("\n[BOT] Recibida señal de terminación. Desconectando...")
    loop = asyncio.get_event_loop()
    loop.create_task(shutdown_bot())

signal.signal(signal.SIGINT, signal_handler)

@bot.event
async def on_ready():
    
    print(f"[BOT] Conectado como {bot.user}")
    await bot.load_extension("cogs.commands")

    await registrar_comandos()


async def shutdown_bot():
    await limpiar_comandos()
    await bot.tree.sync(guild=None)  # Sincronización de comandos globales
    print("[BOT] Comandos globales actualizados correctamente.")
    print("[BOT] Desconectando...")
    await bot.close()

async def limpiar_comandos():
    try:
        print("[BOT] Limpiando comandos...")
        bot.tree.clear_commands(guild=None)
        await bot.tree.sync(guild=None)  # Limpieza de comandos
        print("[BOT] Comandos limpiados correctamente.")
    except Exception as e:
        print(f"[BOT] Error al limpiar comandos. Trace: {e}")

async def registrar_comandos():
    try:
        print("[BOT] Registrando comandos...")
        await bot.tree.sync()  # Registro de comandos
        print(f"[BOT] Comandos registrados correctamente. {len(bot.tree.get_commands())} comandos registrados.")
    except Exception as e:
        print(f"[BOT] Error al registrar comandos. Trace: {e}")
bot.run(TOKEN)