import discord
from discord.ext import commands
import asyncio
import youtube_dl
if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    discord.opus.load_opus('opus')


class Music:
    def __init__(self, bot):
        self.bot = bot
        self.voice_states = []

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state

    async def create_voice_client(self, channel):
        voice = await self.bot.join_voice_channel(channel)
        state = self.get_voice_state(channel.server)
        state.voice = voice

    @commands.command(pass_context=True, no_pm=True)
    async def summon(self, ctx):
        """Summons the bot to join your voice channel."""
        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            await self.bot.say('You are not in a voice channel.')
            return False
        if state.voice is None:
            state.voice = await self.bot.join_voice_channel(summoned_channel)
        else:
            await state.voice.move_to(summoned_channel)

        return True
    @commands.command(pass_context=True, no_pm=True)
    async def playtest(self,ctx, *,song : str):
        """plays a song."""
        state = self.get_voice_state(ctx.message.server)
        author = ctx.message.author.voice_channel
        channel = ctx.message.channel
        player = await state.voice.create_ytdl_player(song, ytdl_options=None, **kwargs)
        player.start()
        

def setup(bot):
    n = Music(bot)
    bot.add_cog(n)
