import discord
from discord.ext import commands
from .utils import checks
import datetime
import random
from __main__ import send_cmd_help, settings

class prune:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, no_pm=True, aliases=['purge'])
    @checks.admin_or_permissions(manage_messages=True)
    async def prune(self, ctx):
        """Prunes messages that meet a criteria."""

        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    async def do_removal(self, message, limit, predicate):
        deleted = await self.bot.purge_from(message.channel, limit=limit, before=message, check=predicate)
        messages = ['%s %s pruned.' % (len(deleted), 'message was' if len(deleted) == 1 else 'messages were')]
        if len(deleted):
            messages.append('')
            removed = 0
            await self.bot.delete_message(message)

        await self.bot.say('\n'.join(messages), delete_after=10)

    @prune.command(pass_context=True)#ratelimits D:
    async def embeds(self, ctx, search=100):
        """prunes messages that have embeds in them."""
        await self.do_removal(ctx.message, search, lambda e: len(e.embeds))

    @prune.command(pass_context=True)#lambda took me long to firgure out files
    async def files(self, ctx, search=100):
        """prunes messages that have attachments in them."""
        await self.do_removal(ctx.message, search, lambda e: len(e.attachments))

    @prune.command(pass_context=True)
    async def images(self, ctx, search=100):
        """prunes messages that have embeds or attachments."""
        await self.do_removal(ctx.message, search, lambda e: len(e.embeds) or len(e.attachments))

    @prune.command(name='all', pass_context=True)
    async def _remove_all(self, ctx, search=100):
        """prunes all messages."""
        await self.do_removal(ctx.message, search, lambda e: True)

    @prune.command(pass_context=True)
    async def user(self, ctx, member : discord.Member, search=100):
        """prunes all messages by the member."""
        await self.do_removal(ctx.message, search, lambda e: e.author == member)

    @prune.command(pass_context=True)
    async def contains(self, ctx, *, substr : str):
        """prunes all messages containing a substring.

        The substring must be at least 3 characters long.
        """
        if len(substr) < 1:
            await self.bot.say('The substring length must be at least 3 characters.')
            return

        await self.do_removal(ctx.message, 100, lambda e: substr in e.content)

    @prune.command(name='bot', pass_context=True)
    async def _bot(self, ctx, prefix, *, member: discord.Member):
        """prunes a bot user's messages and messages with their prefix.

        The member doesn't have to have the [Bot] tag to qualify for removal.
        """

        def predicate(m):
            return m.author == member or m.content.startswith(prefix)
        await self.do_removal(ctx.message, 100, predicate)


def setup(bot):
    n = prune(bot)
    bot.add_cog(n)
