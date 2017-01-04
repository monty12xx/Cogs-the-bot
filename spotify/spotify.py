import discord
import time
from discord.ext import commands
from random import choice, randint
import cogs.utils
import asyncio
from cogs.utils import checks
class disco:
    """Disco role"""

    def __init__(self, bot):
        self.bot = bot
    @checks.is_owner()
    @commands.command(pass_context = True, no_pm=True)
    async def discorole(self, ctx, times : int,  *, role: discord.Role):
        """only only donators !. if you want this to work contact bot owner , or donate."""
        time = 0
        while time < times:
            colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
            colour = int(colour, 16)
            await self.bot.edit_role(ctx.message.server, role, colour=discord.Colour(value=colour))
            time = time + 1
            await asyncio.sleep(8.5)
	
    @checks.is_owner()
    @commands.command(pass_context = True, no_pm=True)
    async def disco(self, ctx, *, role: discord.Role):
        """only only donators !. if you want this to work contact bot owner , or donate."""
        while True:
            colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
            colour = int(colour, 16)
            await self.bot.edit_role(ctx.message.server, role, colour=discord.Colour(value=colour))
            await asyncio.sleep(8.5)


def setup(bot):
    n = disco(bot)
    bot.add_cog(n)
