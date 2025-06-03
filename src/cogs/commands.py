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
async def setup(bot):
    await bot.add_cog(Comandos(bot))