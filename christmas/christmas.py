import discord
from discord.ext import commands
import asyncio


class christmas:
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True, No_Pm=True)
    async def christmas(self, ctx):
        """happy christmas take this gift <3"""
        channel = ctx.message.channel
        author = ctx.message.author

        a =await self.bot.send_message(channel, "{} merry christmas ! :heart: :christmas_tree: *wait for a surprise*".format(author.mention))
        await asyncio.sleep(2)
        await self.bot.edit_message(a,":christmas_tree: :ribbon: :christmas_tree: :ribbon: :christmas_tree: :ribbon: :christmas_tree:")
        await asyncio.sleep(1.5)
        await self.bot.edit_message(a,":ribbon: :christmas_tree: :ribbon: :christmas_tree: :ribbon: :christmas_tree:  :christmas_tree: ")
        await asyncio.sleep(2)
        await self.bot.edit_message(a,":confetti_ball: :ribbon: :confetti_ball: :christmas_tree: :confetti_ball: :ribbon: :confetti_ball: :christmas_tree: :confetti_ball: :ribbon: :confetti_ball: :christmas_tree: :confetti_ball: :ribbon: :confetti_ball:")
        await asyncio.sleep(1.5)
        await self.bot.edit_message(a,":christmas_tree: :mrs_claus::skin-tone-2: :heart: :christmas_tree: :mrs_claus::skin-tone-2: ")
        await asyncio.sleep(0.5)
        await self.bot.edit_message(a, "{} merry christmas :heart: :tada:".format(author.name))
        return

def setup(bot):
    n = christmas(bot)
    bot.add_cog(n)



