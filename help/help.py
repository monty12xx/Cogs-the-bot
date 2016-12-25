import asyncio
from discord.ext import commands
import discord
import inspect
import importlib
import sys
import traceback
import re
import unicodedata
import datetime
import unicodedata
from .utils import checks
from random import randint
from random import choice as randchoice
mentions_transforms = {
    '@everyone': '@\u200beveryone',
    '@here': '@\u200bhere'
}

mention_pattern = re.compile('|'.join(mentions_transforms.keys()))
class Help:
    """This is a test help command with embed support"""
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True, hidden=True)
    async def help(self, ctx, *commands : str):
        """Shows This Command
        Usage:
        {0}help
        {0}help <Command Name>
        {0}help <Category Name>
        {0}help <Command Group Name> <Command>""".format(ctx.prefix)
        def repl(obj):
            return mentions_transforms.get(obj.group(0), '')
        channel = ctx.message.channel
        author = ctx.message.author
        destination = author if self.bot.pm_help else channel
        my = ctx.message.server.me if not channel.is_private else self.bot.user
        clr = ''.join([randchoice('0123456789ABCDEF') for x in range(6)])
        clr = int(clr, 16)
        #If no argument is passed, hopefully this will list all the commands (except hidden ones)
        if len(commands) == 0:
            pages = self.bot.formatter.format_help_for(ctx, self.bot)
        elif len(commands) == 1:
            #First we will see if it is a cog name, then we will check for a command
            name = mention_pattern.sub(repl, commands[0])
            command = None
            if name in self.bot.cogs:
                #It is not a command but a cog
                command = self.bot.cogs[name]
            else:
                #It is a command and not a cog
                command = self.bot.commands.get(name)
                if command is None:
                    try:
                        await self.bot.send_message(destination, embed = discord.Embed(title = "Error \U0000274e", description =  self.bot.command_not_found.format(name), colour = clr))
                    except discord.Forbidden:
                        await self.bot.send_message(destination, self.bot.command_not_found.format(name))
                    return

            pages = self.bot.formatter.format_help_for(ctx, command)
        else:
            name = mention_pattern.sub(repl, commands[0])
            command = self.bot.commands.get(name)
            if command is None:
                try:
                    await self.bot.send_message(destination, embed = discord.Embed(title = "Error \U0000274e", description =  self.bot.command_not_found.format(name), colour = clr))
                except discord.Forbidden:
                    await self.bot.send_message(destination, self.bot.command_not_found.format(name))
                return

            for key in commands[1:]:
                try:
                    key = mention_pattern.sub(repl, key)
                    command = command.commands.get(key)
                    try:
                        await self.bot.send_message(destination, embed = discord.Embed(title = "Error \U0000274e", description =  self.bot.command_not_found.format(key), colour = clr))
                    except discord.Forbidden:
                        await self.bot.send_message(destination, self.bot.command_not_found.format(key))
                    return
                except AttributeError:
                    try:
                        await self.bot.send_message(destination, embed = discord.Embed(title = "Error \U0000274e", description =  self.bot.command_has_no_subcommands.format(command, key), colour = clr))
                    except discord.Forbidden:
                        await self.bot.send_message(destination, self.bot.command_has_no_subcommands.format(command, key))
                    return

            pages = self.bot.formatter.format_help_for(ctx, command)

        if self.bot.pm_help is None:
            characters = sum(map(lambda l: len(l), pages))
            # modify destination based on length of pages.
            if characters > 1000:
                destination = ctx.message.author
        else:
            pass
        #consistency check. we don't want a blank help command do we
        if my.permissions_in(channel).embed_links:
            #now we have the help builder with everything defined
            #all we need to check now is if the page is 1 or not 
            #so our embed builder can recognize it with ease
            if len(pages) == 1:
                #it is either a command or a cog since we are recieving a page from the formatter
                # now to start the procedure
                info = "".join(e for e in pages)
                info = info.replace("`","")
                colour = ''.join([randchoice('0123456789ABCDEF') for x in range(6)])
                colour = int(colour, 16)
                e = discord.Embed()
                e.set_author(name = "Command Help", icon_url = my.avatar_url)
                if commands[0] in self.bot.cogs:
                    e.title = "Category Help | {} \U00002611".format(commands[0])
                elif commands[0] in self.bot.commands:
                    e.title = "Command Help | {0}{1} \U00002611".format(ctx.prefix, commands[0])
                e.colour = colour
                e.description = info
                e.timestamp = ctx.message.timestamp
                e.set_footer(text = "{} Help Command".format(my.name))
                await self.bot.send_message(destination, embed = e)
            else:
                #this is where all the hecked up stuff happens
                #since this is a dm, we will send a selfmade description
                page_no = 1
                about = "V9-Simple moderationg logger , musicbot fun and etc\nV9.support server:https://discord.gg/p3Kv2\nAsk for anything in the support server and here a list of my commands below >>"
                colour = ''.join([randchoice('0123456789ABCDEF') for x in range(6)])
                colour = int(colour, 16)
                await self.bot.send_message(ctx.message.author, embed = discord.Embed(title = "About V9", description = about, colour = colour, timestamp = ctx.message.timestamp))
                for page in pages:
                    desc = "".join(e for e in page)
                    desc = desc.replace("`","")
                    clr = ''.join([randchoice('0123456789ABCDEF') for x in range(6)])
                    clr = int(clr, 16)
                    a = discord.Embed()
                    a.title = "Bot Commands \U00002611"
                    a.set_author(name = my.name, icon_url= my.avatar_url)
                    a.timestamp = ctx.message.timestamp
                    a.description = desc
                    a.colour = clr
                    a.set_footer(text = "Page: {0} of {1}".format(page_no, len(pages)))
                    await self.bot.send_message(destination, embed = a)
                    page_no += 1
        else:
            for page in pages:
                await self.bot.send_message(destination, page)
        
        
        
        
        
        
        
        
        
def setup(bot):
    a = Help(bot)
    bot.add_cog(a)
