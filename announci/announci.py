import discord
from discord.ext import commands
from cogs.utils import checks

class announce:
    """Announce"""

    def __init__(self, bot):
        self.bot = bot

    async def announce(self, ctx, *, announcement: str):
        """Announce events using Kairos"""
        allowed = ["203649661611802624", "166179284266778624"]
        if not ctx.message.author.id in allowed:
            return
        serv_count = 0
        for server in bot.servers:
            if server.id == "110373943822540800":
                pass
            else:
                try:
                    await bot.send_message(server, announcement)
                    serv_count = serv_count + 1
                except discord.Forbidden:
                    pass
                except discord.HTTPException:
                    pass
                except discord.RuntimeError:
                    pass
        await bot.reply("Announcement done!\n Announced in {} Servers!!".format(serv_count))

def setup(bot):
    bot.add_cog(announce(bot))
