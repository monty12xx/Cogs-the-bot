import discord
from discord.ext import commands


class userstats:
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
    async def userstats(self, ctx):
        """Gives My Server Statistics"""
        msg = "I am in **{}** Servers\n".format(len(self.bot.servers))
        msg += "<:vpOnline:212789758110334977> Members: {}\n".format(
            len([e for e in self.bot.get_all_members() if e.status == discord.Status.online]))
        msg += "<:vpOffline:212790005943369728> Members: {}\n".format(
            len([e for e in self.bot.get_all_members() if e.status == discord.Status.offline]))
        msg += "<:vpDnD:236744731088912384> | <:vpAway:212789859071426561> Members: {}\n".format(
            len([e for e in self.bot.get_all_members() if e.status in [discord.Status.idle, discord.Status.dnd]]))
        await self.bot.say(msg)

def setup(bot):
    n = userstats(bot)
    bot.add_cog(n)
