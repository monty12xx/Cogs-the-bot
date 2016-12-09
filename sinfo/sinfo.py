import discord
from discord.ext import commands
from .utils import checks


class setup:
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
    @checks.serverowner_or_permissions(administrator=True)
    async def setup(self, ctx):
        """setup bot roles.."""
        await self.bot.create_role(server, name='Bot Commander', value=0)
        await self.bot.create_role(server, name='!', value=8)
        await self.bot.say("{}i have created the bot roles\nModRole: Bot Commander\nAdminRole : !".format(author.mention))

def setup(bot):
    n = setup(bot)
    bot.add_cog(n)




