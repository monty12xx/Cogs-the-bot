import discord
from discord.ext import commands
from cogs.utils import checks
from __main__ import set_cog
from .utils.dataIO import dataIO
from .utils.chat_formatting import pagify, box
import random
from random import randint
from random import choice as randchoice
from .utils.chat_formatting import *

import importlib
import traceback
import logging
import asyncio
from copy import deepcopy
import threading
import datetime
import time
import glob
import os
import aiohttp


class party:
    """All owner-only commands that relate to debug bot operations.
    """

    def __init__(self, bot):
        self.bot = bot
        self.setowner_lock = False
        self._announce_msg = None
        self._announce_server = None
        self._settings = dataIO.load_json('data/admin/settings.json')
        self._settable_roles = self._settings.get("ROLES", {})
        self.file_path = "data/red/disabled_commands.json"
        self.disabled_commands = dataIO.load_json(self.file_path)
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    async def _confirm_invite(self, server, owner, ctx):
        answers = ("yes", "y")
        invite = await self.bot.create_invite(server)
        if ctx.message.channel.is_private:
            await self.bot.say(invite)
        else:
            await self.bot.say("Are you sure you want to post an invite to {} "
                               "here? (yes/no)".format(server.name))
            msg = await self.bot.wait_for_message(author=owner, timeout=15)
            if msg is None:
                await self.bot.say("I guess not.")
            elif msg.content.lower().strip() in answers:
                await self.bot.say(invite)
            else:
                await self.bot.say("Alright then.")

    def _is_server_locked(self):
        return self._settings.get("SERVER_LOCK", False)
        
    @commands.command(pass_context=True)
    @checks.is_owner()
    async def sexycrash(self, ctx, idnum=None):
        """Lists servers and generates invites for them"""
        owner = ctx.message.author
        if idnum:
            server = discord.utils.get(self.bot.servers, id=idnum)
            if server:
                await self._confirm_invite(server, owner, ctx)
            else:
                await self.bot.say("I'm not in that server")
        else:
            msg = ""
            servers = sorted(self.bot.servers, key=lambda s: s.name)
            for i, server in enumerate(servers, 1):
                msg += "{}: {}\n".format(i, server.name)
            msg += "\nTo post an invite for a server just type its number."
            for page in pagify(msg, delims=["\n"]):
                await self.bot.say(box(page))
                await asyncio.sleep(1.5)  # Just in case for rate limits
            msg = await self.bot.wait_for_message(author=owner, timeout=15)
            if msg is not None:
                try:
                    msg = int(msg.content.strip())
                    server = servers[msg - 1]
                except ValueError:
                    await self.bot.say("You must enter a number.")
                except IndexError:
                    await self.bot.say("Index out of range.")
                else:
                    try:
                        await self._confirm_invite(server, owner, ctx)
                    except discord.Forbidden:
                        await self.bot.say("I'm not allowed to make an invite"
                                           " for {}".format(server.name))
            else:
                await self.bot.say("Response timed out.")
def setup(bot):
    n = party(bot)
    bot.add_cog(n)
