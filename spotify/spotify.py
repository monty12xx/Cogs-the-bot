import discord
from discord.ext import commands
import spotipy

class spotify:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def spotify(self, ctx, *, content):
        author = ctx.message.author
        sp = spotipy.Spotify()
        a = content
        b = self.bot.say("how much songs?")
        results= sp.search(q=a, limit=b)
        for i, t in enumerate(results['tracks']['items']):
            self.bot.say(' ', i, t['name'])
def setup(bot):
    n = spotify(bot)
    bot.add_cog(n)
