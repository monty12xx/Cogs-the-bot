import discord
from discord.ext import commands
from .utils import checks


class prefix:
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
    async def prefix(self, ctx):
        """setup bot roles.."""
        author = ctx.message.author
        server = ctx.message.server
        p = ("%")
        await self.bot.say("{} my prefixes is{}".format(author.mention, p))


def setup(bot):
    n = prefix(bot)
    bot.add_cog(n)




