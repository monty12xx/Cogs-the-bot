import discord
from discord.ext import commands
from .utils.dataIO import dataIO
from .utils import checks
from __main__ import send_cmd_help, settings
from collections import deque, defaultdict
from cogs.utils.chat_formatting import escape_mass_mentions, box
import os
import re
import logging
import asyncio

class channel:
    def __init__(self, bot):
    self.bot = bot
    

    @commands.group(pass_context=True, no_pm=True, invoke_without_command=True)
    @checks.mod_or_permissions(administrator=True)
    async def bmute(self, ctx, user : discord.Member):
        """Mutes user in the channel/server
        Defaults to channel"""
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.channel_mute, user=user)

    @bmute.command(name="channel", pass_context=True, no_pm=True)
    @checks.mod_or_permissions(administrator=True)
    async def channel_mute(self, ctx, user : discord.Member):
        """Mutes user in the current channel"""
        channel = ctx.message.channel
        overwrites = channel.overwrites_for(user)
        if overwrites.send_messages is False:
            await self.bot.say("That user can't send messages in this "
                               "channel.")
            return
        self._perms_cache[user.id][channel.id] = overwrites.send_messages
        overwrites.send_messages = False
        try:
            await self.bot.edit_channel_permissions(channel, user, overwrites)
        except discord.Forbidden:
            await self.bot.say("Failed to mute user. I need the manage roles "
                               "permission and the user I'm muting must be "
                               "lower than myself in the role hierarchy.")
        else:
            dataIO.save_json("data/mod/perms_cache.json", self._perms_cache)
            await self.bot.say("User has been muted in this channel.")

    @bmute.command(name="server", pass_context=True, no_pm=True)
    @checks.mod_or_permissions(administrator=True)
    async def server_mute(self, ctx, user : discord.Member):
        """Mutes user in the server"""
        server = ctx.message.server
        register = {}
        for channel in server.channels:
            if channel.type != discord.ChannelType.text:
                continue
            overwrites = channel.overwrites_for(user)
            if overwrites.send_messages is False:
                continue
            register[channel.id] = overwrites.send_messages
            overwrites.send_messages = False
            try:
                await self.bot.edit_channel_permissions(channel, user,
                                                        overwrites)
            except discord.Forbidden:
                await self.bot.say("Failed to mute user. I need the manage roles "
                                   "permission and the user I'm muting must be "
                                   "lower than myself in the role hierarchy.")
                return
            else:
                await asyncio.sleep(0.1)
        if not register:
            await self.bot.say("That user is already muted in all channels.")
            return
        self._perms_cache[user.id] = register
        dataIO.save_json("data/mod/perms_cache.json", self._perms_cache)
        await self.bot.say("User has been muted in this server.")

    @commands.group(pass_context=True, no_pm=True, invoke_without_command=True)
    @checks.mod_or_permissions(administrator=True)
    async def bunmute(self, ctx, user : discord.Member):
        """Unmutes user in the channel/server
        Defaults to channel"""
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.channel_unmute, user=user)

    @bunmute.command(name="channel", pass_context=True, no_pm=True)
    @checks.mod_or_permissions(administrator=True)
    async def channel_unmute(self, ctx, user : discord.Member):
        """Unmutes user in the current channel"""
        channel = ctx.message.channel
        overwrites = channel.overwrites_for(user)
        if overwrites.send_messages:
            await self.bot.say("That user doesn't seem to be muted "
                               "in this channel.")
            return
        if user.id in self._perms_cache:
            old_value = self._perms_cache[user.id].get(channel.id, None)
        else:
            old_value = None
        overwrites.send_messages = old_value
        is_empty = self.are_overwrites_empty(overwrites)
        try:
            if not is_empty:
                await self.bot.edit_channel_permissions(channel, user,
                                                        overwrites)
            else:
                await self.bot.delete_channel_permissions(channel, user)
        except discord.Forbidden:
            await self.bot.say("Failed to unmute user. I need the manage roles"
                               " permission and the user I'm unmuting must be "
                               "lower than myself in the role hierarchy.")
        else:
            try:
                del self._perms_cache[user.id][channel.id]
            except KeyError:
                pass
            if user.id in self._perms_cache and not self._perms_cache[user.id]:
                del self._perms_cache[user.id] #cleanup
            dataIO.save_json("data/mod/perms_cache.json", self._perms_cache)
            await self.bot.say("User has been unmuted in this channel.")

    @bunmute.command(name="server", pass_context=True, no_pm=True)
    @checks.mod_or_permissions(administrator=True)
    async def server_unmute(self, ctx, user : discord.Member):
        """Unmutes user in the server"""
        server = ctx.message.server
        if user.id not in self._perms_cache:
            await self.bot.say("That user doesn't seem to have been muted with {0}mute commands. "
                               "Unmute them in the channels you want with `{0}unmute <user>`"
                               "".format(ctx.prefix))
            return
        for channel in server.channels:
            if channel.type != discord.ChannelType.text:
                continue
            if channel.id not in self._perms_cache[user.id]:
                continue
            value = self._perms_cache[user.id].get(channel.id)
            overwrites = channel.overwrites_for(user)
            if overwrites.send_messages is False:
                overwrites.send_messages = value
                is_empty = self.are_overwrites_empty(overwrites)
                try:
                    if not is_empty:
                        await self.bot.edit_channel_permissions(channel, user,
                                                                overwrites)
                    else:
                        await self.bot.delete_channel_permissions(channel, user)
                except discord.Forbidden:
                    await self.bot.say("Failed to unmute user. I need the manage roles"
                                       " permission and the user I'm unmuting must be "
                                       "lower than myself in the role hierarchy.")
                    return
                else:
                    del self._perms_cache[user.id][channel.id]
                    await asyncio.sleep(0.1)
        if user.id in self._perms_cache and not self._perms_cache[user.id]:
            del self._perms_cache[user.id] #cleanup
        dataIO.save_json("data/mod/perms_cache.json", self._perms_cache)
        await self.bot.say("User has been unmuted in this server.")
        
        
        
def setup(bot):
    n = channel(bot)
    bot.add_cog(n)        
