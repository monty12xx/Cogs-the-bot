import discord
from discord.ext import commands

class Shit:
    def __init__(self, bot):
        self.bot = bot
    async def on_server_join(self, server):
        msg = "Thanks for adding me to your server , do %help to see all my commands <3"
        await self.bot.send_message(server, msg)

def setup(bot):
    n = Shit(bot)
    bot.add_cog(n)

