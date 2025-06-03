import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    
    print(f"[BOT] Conectado como {bot.user}")
    await bot.load_extension("cogs.commands")

    try:
        sync = await bot.tree.sync()
        print (f"[BOT] Comandos Slash sincronizados con éxito. {len(sync)}")
    except Exception as e:
        print (f"[BOT] Error al sincronizar los comandos slash. Trace: {e}")

bot.run(TOKEN)