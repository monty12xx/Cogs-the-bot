import discord
from discord.ext import commands
from .utils import checks


class inrole:
    def __init__(self, bot):
        self.bot = bot


    async def role(self, ctx, *, rolename):
        """show how much users in the role"""
        channel = ctx.message.channel
        server = ctx.message.channel
        s = "\n"
        ss = ([x.name for x in server.members if discord.utils.get(server.roles, name = rolename) in x.roles])







def setup(bot):
    n = inrole(bot)
    bot.add_cog(n)
