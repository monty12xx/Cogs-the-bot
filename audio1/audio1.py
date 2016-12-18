import aiohttp
import asyncio
import discord
import youtube_dl
import re
# noinspection PyUnresolvedReferences
from __main__ import send_cmd_help
from discord.ext import commands
from cogs.utils import checks
from cogs.utils.dataIO import dataIO
from cogs.utils import chat_formatting


class BetterAudio:
    """Pandentia's Better Audio"""
    def __init__(self, bot):
        self.bot = bot
        try:
            self.db = dataIO.load_json("./data/better_audio.json")
        except FileNotFoundError:
            self.db = {}
        self.loop = self.bot.loop.create_task(self.maintenance_loop())
        self.playing = {}
        self.queues = {}
        self.skip_votes = {}
        self.voice_clients = {}
        self.players = {}
        self.old_status = None

    def __unload(self):
        self.loop.cancel()

    def save_db(self):
        dataIO.save_json("./data/better_audio.json", self.db)

    def get_eligible_members(self, members):
        eligible = []
        for member in members:
            if not member.bot and not member.self_deaf:
                eligible.append(member)
        return eligible

    def get_url_info(self, url):
        with youtube_dl.YoutubeDL({}) as yt:
            return yt.extract_info(url, download=False, process=False)

    async def maintenance_loop(self):
        while True:
            for server in self.bot.servers:  # set nonexistent voice clients and players to None
                if server.id not in self.players:
                    self.players[server.id] = None
                if server.id not in self.voice_clients:
                    self.voice_clients[server.id] = None
                if server.id not in self.queues:  # create queues
                    self.queues[server.id] = []
                if server.id not in self.db:  # set defaults
                    self.db[server.id] = {"volume": 1.0, "vote_percentage": 0.5}
                if server.id not in self.skip_votes:  # create skip_votes list of Members
                    self.skip_votes[server.id] = []

            for sid in self.players:  # clean up dead players
                player = self.players[sid]
                if player is not None:
                    if player.is_done():
                        self.players[sid] = None
            for sid in self.voice_clients:  # clean up dead voice clients
                voice_client = self.voice_clients[sid]
                if voice_client is not None:
                    if not voice_client.is_connected():
                        self.voice_clients[sid] = None
            for sid in dict(self.playing):  # clean up empty playing messages
                playing = self.playing[sid]
                if playing == {}:
                    self.playing.pop(sid)

            if "global" not in self.db:
                self.db["global"] = {"playing_status": False}
                self.save_db()

            # Queue processing:
            for sid in self.voice_clients:
                voice_client = self.voice_clients[sid]
                player = self.players[sid]
                queue = self.queues[sid]
                if voice_client is not None:
                    if player is None:
                        # noinspection PyBroadException
                        try:
                            self.playing[sid] = {}
                            self.skip_votes[sid] = []
                            next_song = queue.pop(0)
                            url = next_song["url"]
                            self.players[sid] = await self.voice_clients[sid].create_ytdl_player(url)
                            self.players[sid].volume = self.db[sid]["volume"]
                            self.players[sid].start()
                            self.playing[sid]["title"] = next_song["title"]
                            self.playing[sid]["author"] = next_song["author"]
                            self.playing[sid]["url"] = next_song["url"]
                            self.playing[sid]["song_owner"] = next_song["song_owner"]
                            # TODO: Playlists and Now Playing annoucements!
                        except:  # in case something bad happens, crashing the loop is *really* undesirable
                            pass
                    else:
                        if player.volume != self.db[sid]["volume"]:  # set volume while player is playing
                            self.players[sid].volume = float(self.db[sid]["volume"])

                        members = self.get_eligible_members(voice_client.channel.voice_members)
                        if len(members) > 0 and not self.players[sid].is_live:
                            self.players[sid].resume()
                        if len(members) == 0 and not self.players[sid].is_live:
                            self.players[sid].pause()
                        try:
                            possible_voters = len(self.get_eligible_members(voice_client.channel.voice_members))
                            votes = 0
                            for member in voice_client.channel.voice_members:
                                if member in self.skip_votes[sid]:
                                    votes += 1

                            if (votes / possible_voters) > float(self.db[sid]["vote_percentage"]):
                                self.players[sid].stop()
                        except ZeroDivisionError:
                            pass

                if self.db["global"]["playing_status"]:
                    if len(self.playing) == 0:
                        if self.old_status is not None:
                            await self.bot.change_status(game=None)
                            self.old_status = None
                    elif len(self.playing) == 1:
                        # noinspection PyBroadException
                        try:
                            for i in self.playing:
                                if self.playing[i] != {}:
                                    playing = self.playing[i]
                            print(playing)
                            status = "{title} - {author}".format(**playing)
                            if status != self.old_status:
                                await self.bot.change_status(game=discord.Game(name=status))
                                self.old_status = status
                        except:
                            pass
                    else:
                        status = "music on {0} servers".format(len(self.playing))
                        if status != self.old_status:
                            await self.bot.change_status(game=discord.Game(name=status))
                            self.old_status = status
                else:
                    if self.old_status is not None:
                        await self.bot.change_status(game=None)
                        self.old_status = None

            await asyncio.sleep(1)

    @commands.command(pass_context=True, no_pm=True)
    async def np(self, ctx):
        """Shows the currently playing song."""
        if ctx.message.server.id in self.playing:
            playing = self.playing[ctx.message.server.id]
            if self.playing[ctx.message.server.id] == {}:
                playing = None
        else:
            playing = None

        if playing is not None:
            await self.bot.say("I'm currently playing **{title}** by **{author}**.\n"
                               "Link: <{url}>\n"
                               "Added by {song_owner}".format(**playing))
        else:
            await self.bot.say("Nothing currently playing.")

    @commands.command(pass_context=True, name="summon", no_pm=True)
    async def summon_cmd(self, ctx):
        """Summons the bot to your voice channel."""
        if ctx.message.author.voice_channel is not None:
            if self.voice_clients[ctx.message.server.id] is None:
                self.voice_clients[ctx.message.server.id] = \
                    await self.bot.join_voice_channel(ctx.message.author.voice_channel)
                await self.bot.say("Summoned to {0} successfully!".format(str(ctx.message.author.voice_channel)))
            else:
                await self.bot.say("I'm already in your channel!")
        else:
            await self.bot.say("You need to join a voice channel first.")

    @commands.command(pass_context=True, name="play", no_pm=True)
    async def play_cmd(self, ctx, url: str, playlist_length: int=999):
        """Plays a SoundCloud or Twitch link."""
        if self.voice_clients[ctx.message.server.id] is None:
            await self.bot.say("You need to summon me first.")
            return
        if ctx.message.author.voice_channel is None:
            await self.bot.say("You need to be in a voice channel.")
            return
        if re.match(r"^http(s)?\:\/\/soundcloud\.com\/[0-9a-zA-Z\-]*\/[0-9a-zA-Z\-]*", url) or \
                re.match(r"^http(s)?\:\/\/twitch\.tv\/[0-9a-zA-Z\-]*\/[0-9a-zA-Z\-]*", url):  # match supported links
            info = self.get_url_info(url)
            if "entries" in info:
                await self.bot.say("Adding a playlist, this may take a while...")
                placeholder_msg = await self.bot.say("​")
                added = 0
                length = playlist_length
                urls = []
                for i in info["entries"]:
                    if length != 0:
                        urls.append(i["url"])
                        length -= 1

                for url in urls:
                    # noinspection PyBroadException
                    try:
                        info = self.get_url_info(url)
                        title = info["title"]
                        author = info["uploader"]
                        assembled_queue = {"url": url, "song_owner": ctx.message.author, "title": title, "author": author}
                        self.queues[ctx.message.server.id].append(assembled_queue)
                        added += 1
                        placeholder_msg = await self.bot.edit_message(placeholder_msg,
                                                                      "Successfully added {1} - {0} to the queue!"
                                                                      .format(title, author))
                        await asyncio.sleep(1)
                    except:
                        await self.bot.say("Unable to add <{0}> to the queue. Skipping.".format(url))
                await self.bot.say("Added {0} tracks to the queue.".format(added))
            else:
                title = info["title"]
                author = info["uploader"]
                assembled_queue = {"url": url, "song_owner": ctx.message.author, "title": title, "author": author}
                self.queues[ctx.message.server.id].append(assembled_queue)
                await self.bot.say("Successfully added {1} - {0} to the queue!".format(title, author))
        else:
            await self.bot.say("That URL is unsupported right now.")

    @commands.command(pass_context=True, name="queue", no_pm=True)
    async def queue_cmd(self, ctx):
        """Shows the queue for the current server."""
        queue = self.queues[ctx.message.server.id]
        if queue:
            number = 1
            human_queue = ""
            for i in queue:
                human_queue += "**{0}".format(number) + ".** **{author}** - " \
                                                        "**{title}** added by {song_owner}\n".format(**i)
                number += 1
            paged = chat_formatting.pagify(human_queue, "\n")  # pagify the output, so we don't hit the 2000 character
            #                                                    limit
            for page in paged:
                await self.bot.say(page)
        else:
            await self.bot.say("The queue is empty! Queue something with the play command.")

    @commands.command(pass_context=True, name="skip", no_pm=True)
    async def skip_cmd(self, ctx):
        """Registers your vote to skip."""
        if ctx.message.author not in self.skip_votes[ctx.message.server.id]:
            self.skip_votes[ctx.message.server.id].append(ctx.message.author)
            await self.bot.say("Vote to skip registered.")
        else:
            self.skip_votes[ctx.message.server.id].remove(ctx.message.author)
            await self.bot.say("Vote to skip unregistered.")

    @checks.mod_or_permissions(move_members=True)
    @commands.command(pass_context=True, no_pm=True)
    async def stop(self, ctx):
        """Be warned, this clears the queue and stops playback."""
        self.playing[ctx.message.server.id] = {}
        self.queues[ctx.message.server.id] = []
        if self.players[ctx.message.server.id] is not None:
            self.players[ctx.message.server.id].stop()
        await self.bot.say("Playback stopped.")

    @checks.mod_or_permissions(move_members=True)
    @commands.command(pass_context=True, no_pm=True)
    async def forceskip(self, ctx):
        """Skips the current song."""
        if self.players[ctx.message.server.id] is not None:
            self.players[ctx.message.server.id].stop()
            await self.bot.say("Song skipped. Blame {0}.".format(ctx.message.author.mention))

    @checks.mod_or_permissions(move_members=True)
    @commands.command(pass_context=True, no_pm=True)
    async def disconnect(self, ctx):
        """Disconnects the bot from the server."""
        self.playing[ctx.message.server.id] = {}
        if self.players[ctx.message.server.id] is not None:
            self.players[ctx.message.server.id].stop()
        if self.voice_clients[ctx.message.server.id] is not None:
            await self.voice_clients[ctx.message.server.id].disconnect()
            await self.bot.say("Disconnected.")

    @commands.command()
    async def audio_source(self):
        """Where the source code for this audio cog can be found."""
        await self.bot.say("https://github.com/Pandentia/Red-Cogs/")

    @commands.group(name="audioset", pass_context=True, invoke_without_command=True)
    async def audioset_cmd(self, ctx):
        """Sets configuration settings."""
        await send_cmd_help(ctx)

    @checks.mod_or_permissions(move_members=True)
    @audioset_cmd.command(pass_context=True, no_pm=True)
    async def volume(self, ctx, volume: int):
        """Sets the audio volume for this server."""
        if 0 < volume < 200:
            volume /= 100
            self.db[ctx.message.server.id]["volume"] = volume
            self.save_db()
            await self.bot.say("Volume for this server set to {0}%.".format(str(int(volume * 100))))
        else:
            await self.bot.say("Try a volume between 0 and 200%.")

    @checks.mod_or_permissions(move_members=True)
    @audioset_cmd.command(pass_context=True, no_pm=True)
    async def vote_ratio(self, ctx, percentage: int):
        """Sets the vote ratio required to skip a song."""
        percentage /= 100
        if 0 < percentage < 1:
            self.db[ctx.message.server.id]["vote_percentage"] = (percentage / 100)
            self.save_db()
            await self.bot.say("Skip threshold set to {0}%.".format(int(percentage * 100)))
        else:
            await self.bot.say("Try a threshold between 0 and 100.")

    @checks.is_owner()
    @audioset_cmd.command()
    async def status(self):
        """Toggles the playing status messages."""
        if self.db["global"]["playing_status"]:
            self.db["global"]["playing_status"] = False
            self.save_db()
            await self.bot.say("Playing messages disabled.")
        elif not self.db["global"]["playing_status"]:
            self.db["global"]["playing_status"] = True
            self.save_db()
            await self.bot.say("Playing messages enabled.")

    # TODO: global settings? (add them to existing commands maybe?)
    # TODO: Auto-summon the bot into a specific channel?


def setup(bot):
    n = BetterAudio(bot)
    bot.add_cog(n)
