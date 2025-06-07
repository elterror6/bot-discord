import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from utils.salute_utils import load_salute_data, save_salute_data

DATA_FILE = "data/salute_data.json"

class Salute(commands.GroupCog, name="salute"):
    def __init__ (self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
    @app_commands.command(name="activate", description="Activar la funcionalidad de saludo para la guild.")
    @app_commands.describe(chanel="Canal donde se enviará el saludo. Si no se especifica, se usará el canal anteriormente especificado.")
    async def activate (self, interaction: discord.Interaction, chanel: discord.TextChannel = None):
        data = load_salute_data()
        gui = str(interaction.guild.id)

        if gui not in data:
            data[gui] = {
                "salute": "¡Hola! {user}",
                "enabled": True,
                "chanel_id": chanel.id if chanel else None
            }
        else:
            data[gui]["enabled"] = True
        save_salute_data(data)
        response = discord.Embed(title="Saludo activado", description="La funcionalidad de saludo ha sido activada para esta guild.", color=discord.Color.dark_grey())
        await interaction.response.send_message(embed=response)

    @app_commands.command(name="deactivate", description="Desactivar la funcionalidad de saludo para la guild.")
    async def deactivate (self, interaction: discord.Interaction):
        data = load_salute_data()
        gui = str(interaction.guild.id)

        if gui in data:
            data[gui]["enabled"] = False
            save_salute_data(data)
            response = discord.Embed(title="Saludo desactivado", description="La funcionalidad de saludo ha sido desactivada para esta guild.", color=discord.Color.dark_grey())
        else:
            response = discord.Embed(title="Error", description="La funcionalidad de saludo no está activada en esta guild.", color=discord.Color.red())
        
        await interaction.response.send_message(embed=response)
    @app_commands.command(name="set", description="Configurar el mensaje de saludo para la guild.")
    @app_commands.describe(message="Mensaje de saludo. Puedes usar {user} para mencionar al usuario.")
    async def set_salute (self, interaction: discord.Interaction, message: str):
        data = load_salute_data()
        gui = str(interaction.guild.id)

        if gui not in data:
            data[gui] = {
                "salute": message,
                "enabled": True
            }
        else:
            data[gui]["salute"] = message
        save_salute_data(data)
        response = discord.Embed(title="Saludo configurado", description=f"El mensaje de saludo ha sido configurado a: {message}", color=discord.Color.dark_grey())
        await interaction.response.send_message(embed=response)
    @app_commands.command(name="chanel", description="Configurar el canal donde se enviará el saludo.")
    @app_commands.describe(chanel="Canal donde se enviará el saludo.")
    async def set_chanel (self, interaction: discord.Interaction, chanel: discord.TextChannel):
        data = load_salute_data()
        gui = str(interaction.guild.id)

        if gui not in data:
            data[gui] = {
                "salute": "¡Hola! {user}",
                "enabled": True,
                "chanel_id": chanel.id
            }
        else:
            data[gui]["chanel_id"] = chanel.id
        save_salute_data(data)
        response = discord.Embed(title="Canal configurado", description=f"El canal para el saludo ha sido configurado a: {chanel.mention}", color=discord.Color.dark_grey())
        await interaction.response.send_message(embed=response)

async def setup (bot: commands.Bot):
    await bot.add_cog(Salute(bot))