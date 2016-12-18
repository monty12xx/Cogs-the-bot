import discord
from discord.ext import commands
from random import choice, randint


class userstats:
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
    async def userstats(self, ctx):
        """Gives My Server Statistics"""
        author = ctx.message.author
        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)
        Online = len([e for e in self.bot.get_all_members() if e.status == discord.Status.online])
        offline = len([e for e in self.bot.get_all_members() if e.status == discord.Status.offline])
        others = len([e for e in self.bot.get_all_members() if e.status in [discord.Status.idle, discord.Status.dnd]])
        em = discord.Embed(colour=discord.Colour(value=colour))
        em.set_author(name="I am in **{}** Servers\n".format(len(self.bot.servers)), icon_url=author.avatar)
        em.add_field(name="<:vpOnline:212789758110334977> Members:", value=Online)
        em.add_field(name="<:vpOffline:212790005943369728> Members: ", value=offline)
        em.add_field(name="<:vpDnD:236744731088912384> | <:vpAway:212789859071426561> Members: ", value=others)
        await self.bot.say(embed=em)

def setup(bot):
    n = userstats(bot)
    bot.add_cog(n)
