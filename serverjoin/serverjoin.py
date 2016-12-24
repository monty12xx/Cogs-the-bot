import discord
from discord.ext import commands
import asyncio
import time
import datetime
import random
from random import choice, randint


class Onjoin:
    def __init__(self, bot):
        self.bot = bot
    async def on_server_join(self, server):
        """says something when joins server"""
        msg1 = "thanks for adding me to this server ->"
        info = embed_serverjoin(server=server)
        await self.bot.send_message(msg1, embed=info)


        await self.bot.send_message(server, embed=e)

    async def embed_serverjoin(self, server):
        msg = """Thanks to adding me to your server ! `%help` < to see all my commands"""
        modlogs = "if you want to modlog the server just do `%modset` and kick/ban using the bot to log the bans."
        music = "to play a song you can simply type %play <song name> and to skip it %skip\nfor playlists %playlist add <playlist name> + <url>"
        trouble = "if the bot crash or have any prob with your server you can simply %contact <msg> and i will answer as soon as possible"
        colour = ''.join([randchoice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        e = discord.Embed()
        e.title = msg
        e.color = colour
        e.add_field(name="to set up modlogs: ", value=modlogs)
        e.add_field(name="for music: ", value=music)
        e.add_field(name="if something wrong happens", value=trouble)
        e.set_author(name="thanks for adding me to {} =>".format(server.name), url=server.icon_url)
        e.set_footer(text="joined on {}".format(message.timestamp), icon_url=server.icon_url)
        e.timestamp = datetime.datetime.utcnow()
        avatar = self.bot.user.avatar_url if self.bot.user.avatar else self.bot.user.default_avatar_url
        e.set_image(url=avatar)
        return e
    await self.bot.say(embed=e)

def setup(bot):
    n = Onjoin(bot)
    bot.add_cog(n)
