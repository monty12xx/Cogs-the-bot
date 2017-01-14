import discord
from discord.ext import commands
import asyncio
import youtube_dl


class Music:
    def __init__(self, bot):
        self.bot = bot
        self.voice_states = []

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state

    @commands.command(pass_context=True, no_pm=True)
    async def summon(self, ctx):
        """Summons the bot to join your voice channel."""
        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            await self.bot.say('You are not in a voice channel.')
            return False

        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            state.voice = await self.bot.join_voice_channel(summoned_channel)
        else:
            await state.voice.move_to(summoned_channel)

        return True
    @commands.command(pass_context=True, no_pm=True)
    async def playtest(self,ctx, *,song : str):
        """plays a song."""
        author = ctx.message.author.voice_channel
        channel = ctx.message.channel
        player = create_ytdl_player(song, ytdl_options=None, **kwargs)
        player.start()

def setup(bot):
    n = Music(bot)
    bot.add_cog(n)
