import discord
from discord.ext import commands
from cogs.utils.dataIO import dataIO
import random

class test:
    def __init__(self, bot):
        self.bot = bot




    @commands.command(pass_context=True, no_pm=True)
    async def serverinfo(self, ctx):
        colour = ''.join([randchoice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)
        created_at = ("Created on {} ({} days ago!)""".format(server.created_at.strftime("%d %b %Y %H:%M"),passed))
        info_embed = discord.Embed(colour=discord.Colour(value=colour))
        info_embed.set_author(name=server.name + created_at,icon_url=server.icon_url)
        info_embed.add_field(name="Owner", value="<@!{}>".format(server.owner.id))
        info_embed.add_field(name="ID", value=server.id)
        info_embed.add_field(name="Created At", value=str(server.created_at))
        info_embed.add_field(name="Channels", value=len(server.channels))
        info_embed.add_field(name="Members", value=server.member_count)
        info_embed.add_field(name="Roles", value=len(server.roles))
        info_embed.add_field(name="Region", value=str(server.region))
        info_embed.add_field(name="AFK Timeout", value="{} minutes".format(server.afk_timeout / 60).replace(".0", ""))
        info_embed.add_field(name="AFK Channel", value=str(server.afk_channel))
        info_embed.add_field(name="Verification Level", value=str(server.verification_level))
        await self.bot.say(embed=info_embed)
        if len(str(server.emojis)) < 1024 and server.emojis:
            info_embed.add_field(name="Emojis", value=" ".join([str(emoji) for emoji in server.emojis]), inline=False)
        elif len(str(server.emojis)) >= 1024:
            info_embed.add_field(name="Emojis", value="**Error**: _Too many emojis_", inline=False)

def setup(bot):
    n = test(bot)
    bot.add_cog(n)
