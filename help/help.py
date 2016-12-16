import discord
from discord.ext import commands


class help:
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
    async def help(self, ctx):
        """sends a link to my commands."""
        channel = ctx.message.channel
        server = ctx.message.server
        author = ctx.message.author
        await self.bot.send_message(channel, ("{}check your dm ;)".format(author.mention)))
        await self.bot.whisper(author, ("You can find all my commands here:http://pastebin.com/dfyeK0mp\nIf you find a bug glitch or have any idea you can jion my support server: https://discord.gg/DmR6X\nif you want to invite me to yourserver Type %invite <3 enjoy."))

def setup(bot):
    n = help(bot)
    bot.add_cog(n)
