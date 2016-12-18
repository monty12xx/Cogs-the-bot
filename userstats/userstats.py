import discord
from discord.ext import commands
from random import choice, randint


class userstats:
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
    async def userstats(self, ctx):
        """Gives My Server Statistics"""

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)
        msg = "I am in **{}** Servers\n".format(len(self.bot.servers))
        Online = "<:vpOnline:212789758110334977> Members: {}\n".format(
            len([e for e in self.bot.get_all_members() if e.status == discord.Status.online]))
        offline += "<:vpOffline:212790005943369728> Members: {}\n".format(
            len([e for e in self.bot.get_all_members() if e.status == discord.Status.offline]))
        others += "<:vpDnD:236744731088912384> | <:vpAway:212789859071426561> Members: {}\n".format(
            len([e for e in self.bot.get_all_members() if e.status in [discord.Status.idle, discord.Status.dnd]]))
        em = discord.Embed(title=msg, colour=discord.Colour(value=colour))
        em.set_author(name="I am in **{}** Servers\n".format(len(self.bot.servers)), icon_url=author.avatar)
        em.add_field(name="Online users:", value=Online)
        em.add_field(name="Offline users:", value=offline)
        em.add_field(name="Other users:", value=others)
        await bot.say(embed=em)

def setup(bot):
    n = userstats
    bot.add_cog(n)
