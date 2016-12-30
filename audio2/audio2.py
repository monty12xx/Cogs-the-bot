import asyncio
import discord
import copy
import glob

from discord.ext import commands
from .utils.extract_info import Extract, VideoTooBig

if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    discord.opus.load_opus('opus')

donation_spam = {}


INIT0 = '203649661611802624'


class VoiceEntry:

    def __init__(self, message, player):
        self.server = message.server.name
        self.requester = message.author
        self.channel = message.channel
        self.voice_channel = message.author.voice_channel
        self.player = player

    def __str__(self):
        fmt = '**{0.title}** uploaded by {0.uploader} and requested by {1.display_name}'
        duration = self.player.duration
        if duration:
            fmt += ' [length: {0[0]}m {0[1]}s]'.format(divmod(duration, 60))
        return fmt.format(self.player, self.requester)

    def embed(self):
        data = discord.Embed(
            color=discord.Color(value="16727871"),
            description=self.player.webpage_url
        )
        duration = self.player.duration
        data.add_field(name="Uploaded by", value=self.player.uploader)
        data.add_field(name="Requested by", value=self.requester.display_name)
        if duration:
            data.add_field(name="Duration", value='{0[0]}m {0[1]}s'.format(
                divmod(duration, 60)))
        data.set_author(name=self.player.title, url=self.player.webpage_url)
        data.set_thumbnail(url=self.player.thumbnail)
        return data


class VoiceState:

    def __init__(self, bot, cog):
        self.volume = 0.6
        self.stop = False
        self.current = None
        self.voice = None
        self.bot = bot
        self.cog = cog
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.songlist = []
        self.skip_votes = set()
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())
        self.Extract = Extract()

    def votes_needed(self):
        return round(len([i.name for i in self.voice.channel.voice_members if i.name != self.bot.user.name]) * 0.6)

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        try:
            return not player.is_done()
        except AttributeError:
            return False

    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing():
            self.player.stop()

    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    async def disconnect(self, message=False):
        try:
            self.player.stop()
        except:
            pass
        try:
            await self.voice.disconnect()
        except:
            pass
        try:
            self.audio_player.cancel()
        except:
            pass
        try:
            for k, v in copy.copy(self.cog.voice_states).items():
                if v == self:
                    del self.cog.voice_states[k]
        except:
            pass


    async def create_player(self):
        entry = self.current
        # args = 'cache/{}.mp3'.format(entry.display_id)
        await self.Extract.download(entry.player.webpage_url)
        args = glob.glob('cache/{}.*'.format(entry.player.display_id))[0]
        player = self.voice.create_ffmpeg_player(args, after=self.toggle_next)

        # TODO: find a way to iterate over this using getattr and setattr
        player.yt = entry.player.yt
        player.title = entry.player.title
        player.display_id = entry.player.display_id
        player.thumbnail = entry.player.thumbnail
        player.webpage_url = entry.player.webpage_url
        player.download_url = entry.player.download_url
        player.views = entry.player.views
        player.is_live = entry.player.is_live
        player.likes = entry.player.likes
        player.dislikes = entry.player.dislikes
        player.duration = entry.player.duration
        player.uploader = entry.player.uploader

        return player

    async def audio_player_task(self):
        while True:
            self.current = await self.songs.get()
            self.current.player = await self.create_player()
            self.play_next_song.clear()
            try:
                if not self.stop:
                    await self.bot.send_message(self.current.channel, "Now playing")
                    await self.bot.send_message(self.current.channel, embed=self.current.embed())
                self.songlist.pop(0)
            except:
                pass
            self.current.player.volume = self.volume
            self.current.player.start()
            await self.play_next_song.wait()
            if not self.songs.empty() or len(self.voice.channel.voice_members) < 2:
                if self.current.requester.voice_channel is not None:
                    await self.voice.move_to(self.current.requester.voice_channel)
                else:
                    await self.disconnect()
            else:
                await self.disconnect()
                return


class Music:
    """Voice related commands.
    Works in multiple servers at once.
    """

    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot, self)
            self.voice_states[server.id] = state

        return state

    async def create_voice_client(self, channel):
        state = self.get_voice_state(channel.server)
        voice = await self.bot.join_voice_channel(channel)
        state.voice = voice

    def __unload(self):
        for state in self.voice_states.values():
            try:
                state.audio_player.cancel()
                if state.voice:
                    self.bot.loop.create_task(state.voice.disconnect())
            except:
                pass

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
    async def play(self, ctx, *, song: str):
        state = self.get_voice_state(ctx.message.server)
        if state.voice is None or not state.is_playing():
            try:
                await self.summon(ctx)
            except Exception as e:
                await self.bot.say('Error: {}, {}'.format(e.__class__.__name__, e))
                raise Exception
        try:
            entry = await state.Extract.extract(song)
            player = entry
        except VideoTooBig:
            await self.bot.say('video is too long, must be under 1 hour')
            if state.voice is None or not state.is_playing():
                await state.disconnect()
        except Exception as e:
            fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
            await self.bot.send_message(ctx.message.channel, fmt.format(e.__class__.__name__, e))
            if state.voice is None or not state.is_playing():
                await state.disconnect()
        else:
            entry = VoiceEntry(ctx.message, player)
            state.songlist.append(entry)
            await state.songs.put(entry)
            await self.bot.say('Enqueued ' + str(entry))

    @commands.command(pass_context=True, no_pm=True)
    async def volume(self, ctx, value: int):
        """Sets the volume of the currently playing song."""

        if value > 100:
            await self.bot.say('select a value between 0-100 pls')
            return
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.volume = state.volume = value / 100
            await self.bot.say('Set the volume to {:.0%}'.format(player.volume))

    @commands.command(pass_context=True, no_pm=True)
    async def pause(self, ctx):
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.pause()
        else:
            await self.bot.say('not playing anything')
            return
        await self.bot.say('paused current song')

    @commands.command(pass_context=True, no_pm=True)
    async def resume(self, ctx):
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.resume()
        else:
            await self.bot.say('not playing anything')
            return
        await self.bot.say('resumed current song')

    @commands.command(pass_context=True, no_pm=True)
    async def stop(self, ctx):
        server = ctx.message.server
        state = self.get_voice_state(server) 
        if ctx.message.author.server_permissions.mute_members == True or ctx.message.author.id == INIT0:
            state.stop = True
            await state.disconnect()
            await self.bot.say('Stopped the current player')


    @commands.command(pass_context=True, no_pm=True)
    async def skip(self, ctx):
        """Vote to skip a song. The song requester can automatically skip.
        3 skip votes are needed for the song to be skipped.
        """

        state = self.get_voice_state(ctx.message.server)
        if not state.is_playing():
            await self.bot.say('Not playing any music right now...')
            return

        voter = ctx.message.author
        if voter not in state.voice.channel.voice_members and voter.id != INIT0:
            await self.bot.say('you are not in the current playing voice channel')
            return

        if voter == state.current.requester or voter.id == INIT0:
            await self.bot.say('Requester requested skipping song...')
            state.skip()
            return

        if state.current.requester.id == INIT0:
            await self.bot.say('nah this song is good')
            return

        if voter.id not in state.skip_votes:
            state.skip_votes.add(voter.id)
            total_votes = len(state.skip_votes)
            if total_votes >= state.votes_needed():
                await self.bot.say('Skip vote passed, skipping song...')
                state.skip()
            else:
                await self.bot.say('Skip vote added, currently at {}/{}'.format(total_votes, state.votes_needed()))
        else:
            await self.bot.say('You have already voted to skip this song.')

    @commands.command(pass_context=True, no_pm=True)
    async def current(self, ctx):
        state = self.get_voice_state(ctx.message.server)
        if state.current is None:
            await self.bot.say('Not playing anything.')
        else:
            skip_count = len(state.skip_votes)
            embed = state.current.embed().add_field(
                name="Skip count", value="{}/{}".format(skip_count, state.votes_needed()))
            await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def songlist(self, ctx):
        state = self.get_voice_state(ctx.message.server)
        skip_count = len(state.skip_votes)
        data = discord.Embed(
            color=discord.Color(value="16727871"),
            description="Queued songs"
        )
        if len(state.songlist) < 1:
            await self.bot.say("nothing is in the queue currently")
            return
        for i in state.songlist:
            data.add_field(name="{}. {}".format(state.songlist.index(
                i) + 1, i.player.title), value="Skip count: {}/{}".format(skip_count, state.votes_needed()))
        await self.bot.say(embed=data)

    @commands.command()
    async def music(self):
        await self.bot.say('Music commands are in %help, or %help music)


def setup(bot):
    bot.add_cog(Music(bot))
