import discord
from discord.ext import commands


class pogo:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(no_pm=True, pass_context=True)
    async def pogo(self, ctx, rolename, user: discord.Member=None):
        """Adds a role to a user, defaults to author

        Role name must be in quotes if there are spaces."""
        author = ctx.message.author
        channel = ctx.message.channel
        server = ctx.message.server

        if user is None:
            user = author

        role = self._role_from_string(server, rolename)

        if role is None:
            await self.bot.say('That role cannot be found.')
            return

        if not channel.permissions_for(server.me).manage_roles:
            await self.bot.say('I don\'t have manage_roles.')
            return

        if author.id == settings.owner:
            pass
        elif not channel.permissions_for(author).manage_roles:
            raise commands.CheckFailure

        await self.bot.add_roles(user, role)
        await self.bot.say('Added user to team {} to {}'.format(role.name, user.name))

def setup(bot):
    n = pogo(bot)
    bot.add_cog(n)
