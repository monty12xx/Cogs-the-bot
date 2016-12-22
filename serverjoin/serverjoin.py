import discord
from discord.ext import commands

class shit:
    def __init__(self, bot):
        self.bot = bot
    async def on_server_join(server):
        await self.bot.send_message(server, "Thanks for adding me to your server , do %help to see all my commands <3")

def setup(bot):
    n = shit(bot)
    bot.add_cog(n)

