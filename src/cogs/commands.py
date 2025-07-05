import discord
from discord.ext import commands
from discord import app_commands

class Comandos (commands.Cog):
    """
    Clase que contiene los comandos del bot.
    Esta clase hereda de commands.Cog y contiene comandos como ping y avatar.
    """
    
    def __init__(self, bot):
        """
        Inicializa la clase Comandos.
        Args:
            bot (commands.Bot): La instancia del bot de Discord.
        """
        super().__init__()
        self.bot = bot

    @app_commands.command (name="ping", description="Devuelve el ping del bot.")
    async def ping (self, interaction: discord.Interaction):
        """
        Comando que devuelve el ping del bot.
        Args:
            interaction (discord.Interaction): La interacción del usuario con el comando.
        """
        lat = round(self.bot.latency * 1000)
        response = discord.Embed(title="Pong!",description=f"{lat} ms", color=discord.Color.dark_gray())

        await interaction.response.send_message(embed=response)

    @app_commands.command(name="avatar", description="Muestra la foto de perfil del usuario dado.")
    @app_commands.describe(user="Usuario del que quieres ver el avatar.")
    async def avatar(self, interaction: discord.Interaction, user: discord.User = None):
        """
        Comando que muestra la foto de perfil del usuario dado.
        Args:
            interaction (discord.Interaction): La interacción del usuario con el comando.
            user (discord.User, optional): El usuario del que se quiere ver el avatar. Si no se especifica, se usa el usuario que ejecuta el comando.
        """
        if user is None:
            user = interaction.user
        avatar_url = user.display_avatar.url
        response = discord.Embed(title=f"Avatar de {user.name}", color=discord.Color.dark_gray())
        response.set_image(url=avatar_url)

        await interaction.response.send_message(embed=response)

async def setup(bot):
    await bot.add_cog(Comandos(bot))