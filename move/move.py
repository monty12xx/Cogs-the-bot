import discord
from discord.ext import commands
from .utils import checks
import asyncio


class move:
    """moves a user from a channel to another one"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @checks.admin_or_permissions(move_members=True)
    async def move(self, ctx, channel: discord.Channel, *users: discord.Member):
        """move a user to another voice channel
		% "channel" @user ,you can move more than a one user or a bunch of users"""
        for user in users:
            try:
                await self.bot.move_member(user, channel)
                await self.bot.say("Moved **{0}** to **__{1}__**".format(user, channel))
                await asyncio.sleep(1)
            except discord.Forbidden:
                await self.bot.say("I need the moving perms")


def setup(bot):
    n = move(bot)
    bot.add_cog(n)
