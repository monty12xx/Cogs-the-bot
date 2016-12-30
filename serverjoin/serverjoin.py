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
        msg1 = "`-` thanks for adding me to adding me to {}\n`-`for a list of my commands do `%help`\n`-` if anything is wrong with the __bot__ :robot:  please contact me using `%contact`\n`-` for modlogs :hammer: to set them just do `%modset` for a help\n`-` if you are using modlogs please kick and ban using the `-` for trivia games `%trivia <trivia>` to start one\n`-`FeedBack And support here : http://tinyurl.com/hvuq4ah `-`\n `-` thanks for using v9 :heart:".format(server.name)
        await self.bot.send_message(server, msg1)

def setup(bot):
    n = Onjoin(bot)
    bot.add_cog(n)
