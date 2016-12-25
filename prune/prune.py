import discord
from discord.ext import commands
from .utils import checks
import datetime
import random

class prune:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, no_pm=True, aliases=['purge'])
    @checks.admin_or_permissions(manage_messages=True)
    async def prune(self, ctx):
        """Removes messages that meet a criteria.

        In order to use this command, you must have Manage Messages permissions
        or have the Bot Admin role. Note that the bot needs Manage Messages as
        well. These commands cannot be used in a private message.

        When the command is done doing its work, you will get a private message
        detailing which users got removed and how many messages got removed.
        """

        if ctx.invoked_subcommand is None:
            await self.bot.say('Invalid criteria passed "{0.subcommand_passed}"'.format(ctx))

    async def do_removal(self, message, limit, predicate):
        deleted = await self.bot.purge_from(message.channel, limit=limit, before=message, check=predicate)
        spammers = Counter(m.author.display_name for m in deleted)
        messages = ['%s %s removed.' % (len(deleted), 'message was' if len(deleted) == 1 else 'messages were')]
        if len(deleted):
            messages.append('')
            spammers = sorted(spammers.items(), key=lambda t: t[1], reverse=True)
            messages.extend(map(lambda t: '**{0[0]}**: {0[1]}'.format(t), spammers))

        await self.bot.say('\n'.join(messages), delete_after=10)

    @prune.command(pass_context=True)
    async def embeds(self, ctx, search=100):
        """Removes messages that have embeds in them."""
        await self.do_removal(ctx.message, search, lambda e: len(e.embeds))

    @prune.command(pass_context=True)
    async def files(self, ctx, search=100):
        """Removes messages that have attachments in them."""
        await self.do_removal(ctx.message, search, lambda e: len(e.attachments))

    @prune.command(pass_context=True)
    async def images(self, ctx, search=100):
        """Removes messages that have embeds or attachments."""
        await self.do_removal(ctx.message, search, lambda e: len(e.embeds) or len(e.attachments))

    @prune.command(name='all', pass_context=True)
    async def _remove_all(self, ctx, search=100):
        """Removes all messages."""
        await self.do_removal(ctx.message, search, lambda e: True)

    @prune.command(pass_context=True)
    async def user(self, ctx, member : discord.Member, search=100):
        """Removes all messages by the member."""
        await self.do_removal(ctx.message, search, lambda e: e.author == member)

    @prune.command(pass_context=True)
    async def contains(self, ctx, *, substr : str):
        """Removes all messages containing a substring.

        The substring must be at least 3 characters long.
        """
        if len(substr) < 3:
            await self.bot.say('The substring length must be at least 3 characters.')
            return

        await self.do_removal(ctx.message, 100, lambda e: substr in e.content)

    @prune.command(name='bot', pass_context=True)
    async def _bot(self, ctx, prefix, *, member: discord.Member):
        """Removes a bot user's messages and messages with their prefix.

        The member doesn't have to have the [Bot] tag to qualify for removal.
        """

        def predicate(m):
            return m.author == member or m.content.startswith(prefix)
        await self.do_removal(ctx.message, 100, predicate)

    @prune.command(pass_context=True)
    async def adv(self, ctx, *, args: str):
        """A more advanced prune command.

        Allows you to specify more complex prune commands with multiple
        conditions and search criteria. The criteria are passed in the
        syntax of `--criteria value`. Most criteria support multiple
        values to indicate 'any' match. A flag does not have a value.
        If the value has spaces it must be quoted.

        The messages are only deleted if all criteria are met unless
        the `--or` flag is passed.

        Criteria:
          user      A mention or name of the user to remove.
          contains  A substring to search for in the message.
          starts    A substring to search if the message starts with.
          ends      A substring to search if the message ends with.
          bot       A flag indicating if it's a bot user.
          embeds    A flag indicating if the message has embeds.
          files     A flag indicating if the message has attachments.
          emoji     A flag indicating if the message has custom emoji.
          search    How many messages to search. Default 100. Max 2000.
          or        A flag indicating to use logical OR for all criteria.
          not       A flag indicating to use logical NOT for all criteria.
        """
        parser = Arguments(add_help=False, allow_abbrev=False)
        parser.add_argument('--user', nargs='+')
        parser.add_argument('--contains', nargs='+')
        parser.add_argument('--starts', nargs='+')
        parser.add_argument('--ends', nargs='+')
        parser.add_argument('--or', action='store_true', dest='_or')
        parser.add_argument('--not', action='store_true', dest='_not')
        parser.add_argument('--emoji', action='store_true')
        parser.add_argument('--bot', action='store_const', const=lambda m: m.author.bot)
        parser.add_argument('--embeds', action='store_const', const=lambda m: len(m.embeds))
        parser.add_argument('--files', action='store_const', const=lambda m: len(m.attachments))
        parser.add_argument('--search', type=int, default=100)

        try:
            args = parser.parse_args(shlex.split(args))
        except Exception as e:
            await self.bot.say(str(e))
            return

        predicates = []
        if args.bot:
            predicates.append(args.bot)

        if args.embeds:
            predicates.append(args.embeds)

        if args.files:
            predicates.append(args.files)

        if args.emoji:
            custom_emoji = re.compile(r'<:(\w+):(\d+)>')
            predicates.append(lambda m: custom_emoji.search(m.content))

        if args.user:
            users = []
            for u in args.user:
                try:
                    converter = commands.MemberConverter(ctx, u)
                    users.append(converter.convert())
                except Exception as e:
                    await self.bot.say(str(e))
                    return

            predicates.append(lambda m: m.author in users)

        if args.contains:
            predicates.append(lambda m: any(sub in m.content for sub in args.contains))

        if args.starts:
            predicates.append(lambda m: any(m.content.startswith(s) for s in args.starts))

        if args.ends:
            predicates.append(lambda m: any(m.content.endswith(s) for s in args.ends))

        op = all if not args._or else any
        def predicate(m):
            r = op(p(m) for p in predicates)
            if args._not:
                return not r
            return r

        args.search = max(0, min(2000, args.search)) # clamp from 0-2000
        await self.do_removal(ctx.message, args.search, predicate)

def setup(bot):
    n = prune(bot)
    bot.add_cog(n)
