import discord
from discord.ext import commands
from cogs.utils import checks
from __main__ import set_cog
from .utils.dataIO import dataIO
from .utils.chat_formatting import pagify, box

import importlib
import traceback
import logging
import asyncio
import threading
import datetime
import glob
import os
import aiohttp



class serverprefix:
    def __init__(self, bot):
        self.bot = bot
    @commands.command(pass_context=True, no_pm=True)
    @checks.serverowner_or_permissions(administrator=True)
    async def serverprefix(self, ctx, *prefixes):
        """Sets V9's prefixes for this server
        Accepts multiple prefixes separated by a space. Enclose in double
        quotes if a prefix contains spaces.
        Example: set serverprefix ! $ ? "two words"
        Issuing this command with no parameters will reset the server
        prefixes and the global ones will be used instead."""
        server = ctx.message.server

        if prefixes == ():
            self.bot.settings.set_server_prefixes(server, [])
            self.bot.settings.save_settings()
            current_p = ", ".join(self.bot.settings.prefixes)
            await self.bot.say("Server prefixes reset. Current prefixes: "
                               "`{}`".format(current_p))
            return

        prefixes = sorted(prefixes, reverse=True)
        self.bot.settings.set_server_prefixes(server, prefixes)
        self.bot.settings.save_settings()
        log.debug("Setting server's {} prefixes to:\n\t{}"
                  "".format(server.id, self.bot.settings.prefixes))

        p = "Prefixes" if len(prefixes) > 1 else "Prefix"
        await self.bot.say("{} set for this server.\n"
                           "To go back to the global prefixes, do"
                           " `{}set serverprefix` "
                           "".format(p, prefixes[0]))
        
def setup(bot):
    n = serverprefix(bot)
    bot.add_cog(n)
