import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from utils.salute_utils import load_salute_data, save_salute_data

DATA_FILE = "data/salute_data.json"

class Salute(commands.GroupCog, name="salute"):
    """
    Clase que maneja los comandos relacionados con la funcionalidad de saludo.
    Esta clase hereda de commands.GroupCog y contiene comandos para activar, desactivar, configurar el mensaje de saludo y el canal donde se enviará el saludo.
    """
    def __init__ (self, bot: commands.Bot):
        """
        Inicializa la clase Salute.
        Args:
            bot (commands.Bot): La instancia del bot de Discord.
        """
        super().__init__()
        self.bot = bot

    @app_commands.command(name="activate", description="Activar la funcionalidad de saludo para la guild.")
    @app_commands.describe(chanel="Canal donde se enviará el saludo. Si no se especifica, se usará el canal anteriormente especificado.")
    async def activate (self, interaction: discord.Interaction, chanel: discord.TextChannel = None):
        """
        Comando que activa la funcionalidad de saludo para la guild.
        Args:
            interaction (discord.Interaction): La interacción del usuario con el comando.
            chanel (discord.TextChannel, optional): El canal donde se enviará el saludo. Si no se especifica, se usará el canal anteriormente configurado.
        """
        data = load_salute_data()
        gui = str(interaction.guild.id)

        if gui not in data:
            data[gui] = {
                "salute": "¡Hola! {user}",
                "enabled": True,
                "chanel_id": chanel.id if chanel else interaction.channel.id
            }
        else:
            data[gui]["enabled"] = True
        save_salute_data(data)
        response = discord.Embed(title="Saludo activado", description="La funcionalidad de saludo ha sido activada para esta guild.", color=discord.Color.dark_grey())
        await interaction.response.send_message(embed=response)

    @app_commands.command(name="deactivate", description="Desactivar la funcionalidad de saludo para la guild.")
    async def deactivate (self, interaction: discord.Interaction):
        """
        Comando que desactiva la funcionalidad de saludo para la guild.
        Args:
            interaction (discord.Interaction): La interacción del usuario con el comando.
        """
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
        """
        Comando que configura el mensaje de saludo para la guild.
        Args:
            interaction (discord.Interaction): La interacción del usuario con el comando.
            message (str): El mensaje de saludo. Puedes usar {user} para mencionar al usuario.
        """
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
        """
        Comando que configura el canal donde se enviará el saludo.
        Args:
            interaction (discord.Interaction): La interacción del usuario con el comando.
            chanel (discord.TextChannel): El canal donde se enviará el saludo.
        """
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
    """
    Carga la extensión de saludo en el bot.
    Args:
        bot (commands.Bot): La instancia del bot de Discord.
    """
    await bot.add_cog(Salute(bot))