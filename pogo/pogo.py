from discord.ext import commands
from random import choice, randint
import requests
import json
import discord
class youtube:
    """youtube"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def youtube(self, ctx, channelname):
        payload = {"q" : channelname, "key" : "AIzaSyCWHEWGj6JS6l8tJs94TG3QWB_gM_1dCEM", "part" : "snippet", "type" : "channel", "maxResults" : 1}
        r = requests.get("https://www.googleapis.com/youtube/v3/search", params = payload)
        idjson = r.content
        decoded1 = idjson.decode("utf-8")
        jsonloaded1 = json.loads(decoded1)
        try:
            channelid = (jsonloaded1["items"][0]['id']['channelId'])
            thumbnail = (jsonloaded1['items'][0]['snippet']['thumbnails']['default']['url'])
            channeln = (jsonloaded1['items'][0]['snippet']['title'])
            payload = {"part" : "statistics",  "id" : channelid, "key" : "AIzaSyCWHEWGj6JS6l8tJs94TG3QWB_gM_1dCEM"}
            b = requests.get("https://www.googleapis.com/youtube/v3/channels", params = payload)
            stats = b.content
            decoded2 = stats.decode("utf-8")
            jsonloaded2 = json.loads(decoded2)
            subscount = jsonloaded2["items"][0]['statistics']['subscriberCount']
            viewcount = jsonloaded2["items"][0]['statistics']['viewCount']
            videocount = jsonloaded2["items"][0]['statistics']['videoCount']
            colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
            colour = int(colour, 16)
            em = discord.Embed(colour=discord.Colour(value=colour))
            em.add_field(name="youtuber", value=channeln)
            em.add_field(name="Views:", value=viewcount)
            em.add_field(name="Subscribers:", value=subscount)
            em.add_field(name="Videos:", value=videocount)
            em.set_author(name=channeln + ":", url=thumbnail, icon_url=thumbnail)
            em.set_thumbnail(url=thumbnail)
            await self.bot.say(embed=em)
        except IndexError:
            await self.bot.say("No such youtuber found")


def setup(bot):
    n = youtube(bot)
    bot.add_cog(n)
