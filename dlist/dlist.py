import json
import discord
from discord.ext import commands
import aiohttp
from cogs.utils import checks

class Discordlist:
    def __init__(self, bot):
        self.bot = bot
    @checks.is_owner()
    @commands.command(pass_context=True)
    async def dlist(self, ctx):
        data = {
            "token" : 'XgoA1YxWUf',
            "servers" : len(bot.servers)
        }
        url = "https://bots.discordlist.net/api.php"
        resp = await.aiohttp.post(url, data=data)
        resp.close()
        await self.bot.say(url.encode(encoding='utf-8'))


def setup(bot):
    n = Discordlist(bot)
    bot.add_cog(n)














