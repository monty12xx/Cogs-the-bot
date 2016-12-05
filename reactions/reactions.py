from discord.ext import commands
from .utils.dataIO import dataIO
from .utils import checks

from __main__ import send_cmd_help, settings
from collections import deque, defaultdict
from cogs.utils.chat_formatting import escape_mass_mentions, box

import os
import discord

class Reaction:


    def __init__(self,bot):
        self.bot = bot
        self.file_path = "data/emoji/emojis.json"
        self.emojis = dataIO.load_json(self.file_path)


    @commands.group(pass_context=True, no_pm=True)
    async def reaction(self,ctx):
        """Reaction commands \n [p]react <emoji>  <user>  <how many messages>"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)


    @commands.command(pass_context=True, no_pm=True,name="react")
    async def react(self, ctx, emoji, numOfMsgs: int = None, user: discord.User = None):
        """Reaction commands \n [p]react <emoji>  <user>  <how many messages>"""
        if numOfMsgs is None:
            num = 1
        else:
            num = numOfMsgs
        if emoji is None:
            await self.bot.send_cmd_help(ctx)
        elif user is None:
            await ctx.invoke(self._react, emoji, num)
        elif user is not None:
            await ctx.invoke(self._react,emoji, num, user)
                
        
    @commands.command(pass_context=True, no_pm=True)
    async def _react(self, ctx, emoji, numOfMsgs: int = None, user: discord.Member = None):
        counter = 0
        acn = 0
        if numOfMsgs is None:
            num = 1
        else:
            num = numOfMsgs
        if num > 15 and not ctx.message.channel.permissions_for(ctx.message.author).manage_messages:
            return await self.bot.say("`You can only .react up to 15 messages.`")
        if user is not None:
            acn = num
            num = 100
        async for msg in self.bot.logs_from(ctx.message.channel, limit=num, before=ctx.message):
            if user is not None and msg.author is not user:
                pass
            else:
                if user is not None and counter >= acn:
                    return
                if emoji.isalnum():
                    for i in range(len(emoji)):
                        if emoji[i].isalpha():
                            await self.bot.add_reaction(msg, self.emojis[emoji[i].upper()])
                        else:
                            await self.bot.add_reaction(msg, self.emojis[str(emoji[i])])
                else:
                    try:
                        name = emoji.replace('<', '')
                        name = name.replace('>', '')
                        await self.bot.add_reaction(msg, name)
                    except:
                        await self.bot.say("**I don't have this emoji.**")
                counter += 1
                
        self.bot.delete_message(ctx.message)
                
                
    @commands.command(pass_context = True, no_pm=True)
    async def litaf(self, ctx):
        L = "\U0001f1f1"
        I = "\U0001f1ee"
        T = "\U0001f1f9"
        fire = "\U0001f525"
        A = "\U0001f1e6"
        F = "\U0001f1eb"
        ok = "\U0001f44c"

        async for x in self.bot.logs_from(ctx.message.channel, before=ctx.message.timestamp, limit=1):
            await self.bot.add_reaction(x, L)
            await self.bot.add_reaction(x, I)
            await self.bot.add_reaction(x, T)
            await self.bot.add_reaction(x, fire)
            await self.bot.add_reaction(x, A)
            await self.bot.add_reaction(x, F)
            await self.bot.add_reaction(x, ok)

    @commands.command(pass_context = True, no_pm=True)
    async def sotru(self, ctx):
        S = "\U0001f1f8"
        U = "\U0001f1fa"
        O = "\U0001f1f4"
        R = "\U0001f1f7"
        L = "\U0001f1f1"
        I = "\U0001f1ee"
        T = "\U0001f1f9"
        fire = "\U0001f525"
        A = "\U0001f1e6"
        F = "\U0001f1eb"
        ok = "\U0001f44c"
        clap = "\U0001f44f"

        async for x in self.bot.logs_from(ctx.message.channel, before=ctx.message.timestamp, limit=1):
            await self.bot.add_reaction(x, S)
            await self.bot.add_reaction(x, O)
            await self.bot.add_reaction(x, clap)
            await self.bot.add_reaction(x, T)
            await self.bot.add_reaction(x, R)
            await self.bot.add_reaction(x, U)
            await self.bot.add_reaction(x, ok)
    @commands.command(pass_context = True, no_pm=True)
    async def idgaf(self, ctx):
        S = "\U0001f1f8"
        U = "\U0001f1fa"
        D = "\U0001f1e9"
        G = "\U0001f1ec"
        O = "\U0001f1f4"
        R = "\U0001f1f7"
        L = "\U0001f1f1"
        I = "\U0001f1ee"
        T = "\U0001f1f9"
        fire = "\U0001f525"
        A = "\U0001f1e6"
        F = "\U0001f1eb"
        ok = "\U0001f44c"
        clap = "\U0001f44f"
        cool = "\U0001f60e"

        async for x in self.bot.logs_from(ctx.message.channel, before=ctx.message.timestamp, limit=1):
            await self.bot.add_reaction(x, I)
            await self.bot.add_reaction(x, D)
            await self.bot.add_reaction(x, G)
            await self.bot.add_reaction(x, A)
            await self.bot.add_reaction(x, F)
            await self.bot.add_reaction(x, cool)
    @commands.command(pass_context = True, no_pm=True)
    async def lmao(self, ctx):
        L = "\U0001f1f1"
        M = "\U0001f1f2"
        A = "\U0001f1e6"
        O = "\U0001f1f4"
        joy = "\U0001f602"
        cjoy = "\U0001f639"

        async for x in self.bot.logs_from(ctx.message.channel, before=ctx.message.timestamp, limit=1):
            await self.bot.add_reaction(x, L)
            await self.bot.add_reaction(x, M)
            await self.bot.add_reaction(x, A)
            await self.bot.add_reaction(x, O)
            await self.bot.add_reaction(x, joy)
            await self.bot.add_reaction(x, cjoy)

    @commands.command(pass_context = True, no_pm=True)
    async def rekt(self, ctx):
        R = "\U0001f1f7"
        E = "\U0001f1ea"
        K = "\U0001f1f0"
        T = "\U0001f1f9"
        FINGERMIDDLE = "\U0001f595"
        FINGERCROSS = "\U0001f91e"

        async for x in self.bot.logs_from(ctx.message.channel, before=ctx.message.timestamp, limit=1):
            await self.bot.add_reaction(x, R)
            await self.bot.add_reaction(x, E)
            await self.bot.add_reaction(x, K)
            await self.bot.add_reaction(x, T)
            await self.bot.add_reaction(x, FINGERMIDDLE)
            await self.bot.add_reaction(x, FINGERCROSS)

    @commands.command(pass_context = True, no_pm=True)
    async def noscope(self, ctx):
        N = "\U0001f1f3"
        BOOM = "\U0001f4a5"
        S = "\U0001f1f8"
        C = "\U0001f595"
        O = "\U0001f1f4"
        P = "\U0001f1f5"
        E = "\U0001f1ea"
        GLASSES = "\U0001f576"

        async for x in self.bot.logs_from(ctx.message.channel, before=ctx.message.timestamp, limit=1):
            await self.bot.add_reaction(x, N)
            await self.bot.add_reaction(x, O)
            await self.bot.add_reaction(x, BOOM)
            await self.bot.add_reaction(x, S)
            await self.bot.add_reaction(x, C)
            await self.bot.add_reaction(x, O)
            await self.bot.add_reaction(x, P)
            await self.bot.add_reaction(x, E)
            await self.bot.add_reaction(x, GLASSES)

    @commands.command(pass_context = True, no_pm=True)
    async def fucker(self, ctx):
        MIDDLEFINGER = "\U0001f595"
        F = "\U0001f1eb"
        U = "\U0001f1fa"
        C = "\U0001f1e8"
        K = "\U0001f1f0"
        Y = "\U0001f1fe"
        O = "\U0001f1f4"
        E = "\U0001f1ea"
        R = "\U0001f1f7"
        point = "\U0001f446"
        FIST = "\U0001f91c"
        bump = "\U0001f91b"

        async for x in self.bot.logs_from(ctx.message.channel, before=ctx.message.timestamp, limit=1):
            await self.bot.add_reaction(x, MIDDLEFINGER)
            await self.bot.add_reaction(x, F)
            await self.bot.add_reaction(x, U)
            await self.bot.add_reaction(x, C)
            await self.bot.add_reaction(x, K)
            await self.bot.add_reaction(x, E)
            await self.bot.add_reaction(x, R)
            await self.bot.add_reaction(x, bump)
    @reaction.command(pass_context=True,no_pm=True)
    async def remove(self,ctx,emoji, numOfMessages: int):
        async for msg in self.bot.logs_from(ctx.message.channel, limit=numOfMessages, before=ctx.message):
            if emoji.isalnum():
                for i in range(len(emoji)):
                    if emoji[i].isalpha():
                        await self.bot.remove_reaction(msg, self.emojis[emoji[i].upper()], self.bot)
                    else:
                        await self.bot.remove_reaction(msg, self.emojis[str(emoji[i])], self.bot)
            else:
                try:
                    name = emoji.replace('<', '')
                    name = name.replace('>', '')
                    await self.bot.remove_reaction(msg, name, self.bot)
                except:
                    pass

        
    # async def return_messages(self,num: int,message, user: discord.User=None):
    #     msgList = []
    #     async for msg in self.bot.logs_from(message.channel, limit=num, before=message):
    #         if user is not None:
    #             if msg.author is user:
    #                 msgList.append(msg)
    #         else:
    #             msgList.append(msg)
    #     return msgList
        
    # async def attach_reactions(self,args,msg):
    #     for emoji in args:
    #         if emoji.isalnum():
    #             for i in range(len(emoji)):
    #                 if emoji[i].isalpha():
    #                     await self.bot.add_reaction(msg, self.emojis[emoji[i].upper()])
    #                 else:
    #                     await self.bot.add_reaction(msg, self.emojis[str(emoji[i])])
    #         else:
    #             try:
    #                 name = emoji.replace('<', '')
    #                 name = name.replace('>', '')
    #                 await self.bot.add_reaction(msg, name)
    #             except:
    #                  await self.bot.say("**I don't have this emoji.**")


def check_folders():
    if not os.path.exists("data/emoji"):
        print("Creating data/emoji folder...")
        os.makedirs("data/emoji")


def check_files():
    letterEmojis = {
        "0": "0\u20e3",
        "1": "1\u20e3",
        "2": "2\u20e3",
        "3": "3\u20e3",
        "4": "4\u20e3",
        "5": "5\u20e3",
        "6": "6\u20e3",
        "7": "7\u20e3",
        "8": "8\u20e3",
        "9": "9\u20e3",
        "A": "\ud83c\udde6",
        "B": "\ud83c\udde7",
        "C": "\ud83c\udde8",
        "D": "\ud83c\udde9",
        "E": "\ud83c\uddea",
        "F": "\ud83c\uddeb",
        "G": "\ud83c\uddec",
        "H": "\ud83c\udded",
        "I": "\ud83c\uddee",
        "J": "\ud83c\uddef",
        "K": "\ud83c\uddf0",
        "L": "\ud83c\uddf1",
        "M": "\ud83c\uddf2",
        "N": "\ud83c\uddf3",
        "O": "\ud83c\uddf4",
        "P": "\ud83c\uddf5",
        "Q": "\ud83c\uddf6",
        "R": "\ud83c\uddf7",
        "S": "\ud83c\uddf8",
        "T": "\ud83c\uddf9",
        "U": "\ud83c\uddfa",
        "V": "\ud83c\uddfb",
        "W": "\ud83c\uddfc",
        "X": "\ud83c\uddfd",
        "Y": "\ud83c\uddfe",
        "Z": "\ud83c\uddff"
    }
    
    f = "data/emoji/emojis.json"
    if not dataIO.is_valid_json(f):
        print("Creating empty emojis.json...")
        dataIO.save_json(f, letterEmojis)

def setup(bot):
    check_folders()
    check_files()
    n = Reaction(bot)
    #bot.add_listener(n.checkCC, "on_message")
    bot.add_cog(n)
