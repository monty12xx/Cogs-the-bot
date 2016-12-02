import discord
from discord.ext import commands
from cogs.utils.dataIO import dataIO
import random
from random import randint
from random import choice as randchoice

class test:
    def __init__(self, bot):
        self.bot = bot




    @commands.command(pass_context=True, no_pm=True)
    async def serverinfo(self, ctx):
        colour = ''.join([randchoice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)
        passed = (ctx.message.timestamp - server.created_at).days
        created_at = ("Created on {} ({} days ago!)""".format(server.created_at.strftime("%d %b %Y %H:%M"),passed))
        em = discord.Embed(description= created_at, colour=discord.Colour(value=colour))
        em.set_author(name=server.name,icon_url=server.icon_url)
        em.add_field(name="Owner", value="<@!{}>".format(server.owner.id))
        em.add_field(name="ID", value=server.id)
        em.add_field(name="Created At", value=str(server.created_at))
        em.add_field(name="Channels", value=len(server.channels))
        em.add_field(name="Members", value=server.member_count)
        em.add_field(name="Roles", value=len(server.roles))
        em.add_field(name="Region", value=str(server.region))
        em.add_field(name="AFK Timeout", value="{} minutes".format(server.afk_timeout / 60).replace(".0", ""))
        em.add_field(name="AFK Channel", value=str(server.afk_channel))
        em.add_field(name="Verification Level", value=str(server.verification_level))
        em.set_thumbnail(url=sever.icon_url)
        await self.bot.say(embed=em)
        if len(str(server.emojis)) < 1024 and server.emojis:
            em.add_field(name="Emojis", value=" ".join([str(emoji) for emoji in server.emojis]), inline=False)
        elif len(str(server.emojis)) >= 1024:
            em.add_field(name="Emojis", value="**Error**: _Too many emojis_", inline=False)

def setup(bot):
    n = test(bot)
    bot.add_cog(n)
