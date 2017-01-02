import discord
from discord.ext import commands
import spotipy

class spotify:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def spotify(self,ctx, *, content, limit):
        sp = spotipy.Spotify()
        a = content
        b = limit
        results= sp.search(q=a, limit=b)
        for i, t in enumerate(results['tracks']['items']):
            await self.bot.say(' ', i, t['name'])
def setup(bot):
    n = spotify(bot)
    bot.add_cog(n)
