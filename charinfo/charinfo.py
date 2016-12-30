import discord
from discord.ext import commands
import unicodedata


class charinfo:
    """charinfo emojis"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def charinfo(self, *, characters: str):
        """Shows info about emojis numbers ,etc
        limit is 20
        """

        if len(characters) > 20:
            await self.bot.say('Too many characters ({}/20)'.format(len(characters)))
            return

        fmt = '`\\U{0:>08}`: {1} - {2} \N{EM DASH} <http://www.fileformat.info/info/unicode/char/{0}>'

        def to_string(c):
            digit = format(ord(c), 'x')
            name = unicodedata.name(c, 'Name not found.')
            return fmt.format(digit, name, c)

        await self.bot.say('\n'.join(map(to_string, characters)))

def setup(bot):
    n = charinfo(bot)
    bot.add_cog(n)
