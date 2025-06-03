import discord
from discord.ext import commands
from discord import app_commands

class Comandos (commands.Cog):
    
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @app_commands.command (name="ping", description="Devuelve el ping del bot.")
    async def ping (self, interaction: discord.Interaction):
        lat = round(self.bot.latency * 1000)
        response = discord.Embed(title="Pong!",description=f"{lat} ms", color=discord.Color.dark_gray())

        await interaction.response.send_message(embed=response)

    @app_commands.command(name="avatar", description="Muestra la foto de perfil del usuario dado.")
    @app_commands.describe(user="Usuario del que quieres ver el avatar.")
    async def avatar(self, interaction: discord.Interaction, user: discord.User = None):
        if user is None:
            user = interaction.user
        avatar_url = user.display_avatar.url
        response = discord.Embed(title=f"Avatar de {user.name}", color=discord.Color.dark_gray())
        response.set_image(url=avatar_url)

        await interaction.response.send_message(embed=response)

async def setup(bot):
    await bot.add_cog(Comandos(bot))