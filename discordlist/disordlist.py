import requests
import json
import discord
from discord.ext import commands
from cogs.utils import checks

class updateservers:
    """updateservers"""

    def __init__(self, bot):
        self.bot = bot

    @checks.is_owner()
    @commands.command()
    async def updateservers(self):
        """updateservers"""
        thepostdata ={
            "server_count": int(len(self.bot.servers))
        }
        r = requests.post("https://bots.discord.pw/api/bots/234179578229293057/stats", headers={'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySUQiOiIyMDM2NDk2NjE2MTE4MDI2MjQiLCJyYW5kIjoxMTAsImlhdCI6MTQ4MjMyNzgzN30.V0Gs1xlGM4ObeX9LfSYzyJwicxuQUvom81r1xptCjKk', 'Content-Type' : 'application/json'}, data=json.dumps(thepostdata))
        await self.bot.say(r.content.decode('utf-8'))
        await self.bot.change_presence(game=discord.Game(name="%help | {} servers \U00002764".format(len(self.bot.servers))))

def setup(bot):
    bot.add_cog(updateservers(bot))
