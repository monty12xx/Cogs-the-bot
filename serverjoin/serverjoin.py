import discord
from discord.ext import commands

class Shit:
    def __init__(self, bot):
        self.bot = bot
    async def on_server_join(self, server):
        msg = "Thanks for adding me to your server , do %help to see all my commands\nall my commands start with `%`\n if there is anything wrong with the bot you always do `%contact (whatever is wrong)` that will send me a message :) and ill answer when ever not busy."
        await self.bot.send_message(server, msg)

def setup(bot):
    n = Shit(bot)
    bot.add_cog(n)

