import asyncio
from parsers.parser import *


# from classes.Voice_State import *

class Music_Player:
    def __init__(self, bot, voice):
        self.bot = bot
        self.voice = voice
        self.play_list = asyncio.Queue()
        self.play_next_song = asyncio.Event()
        self.song = None
        self.rec_songs = None
        self.rec_list = []
        self.player = None
        self.volume = 0.1
        self.ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'quiet': True,
        }

    def toggle_next_song(self):
        self.loop.call_soon_threadsafe(self.play_next_song.set)

    def is_playing(self):
        return self.player is not None and self.player.is_playing()

    def pause(self):
        if self.player.is_playing():
            self.player.pause()

    def resume(self):
        if self.player is not None and not self.is_playing():
            self.player.resume()

    def get_info(self, song):
        """Call upon the youtube-dl library to obtain info about the song."""
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            result = ydl.extract_info(song, download=False)

        return result

    async def skip(self, server, channel):
        if self.player.is_playing():
            self.player.stop()
            self.player = None
            await self.play_music(server, channel)

    async def clear(self):
        if self.player.is_playing():
            self.player.stop()
        while not self.play_list.empty():
            await self.play_list.get()

        self.player = None

    async def shuffle(self, channel):
        playlist = []
        while not self.play_list.empty():
            song = await self.play_list.get()
            playlist.append(song)

        shuffle(playlist)

        for song in playlist:
            await self.play_list.put(song)

        await self.send_message(channel, "```Queue has been shuffled.```")

    async def queue(self, channel):
        save_queue = Queue()
        info_list = Queue()
        how_many = 0
        counter = 0
        msg = ""

        if not self.play_list.empty():
            while not self.play_list.empty():
                song = await self.play_list.get()
                info = self.get_info(song)
                info_list.put(info['title'])
                save_queue.put(song)

            length = int(info_list.qsize() / 10)

            while info_list.qsize() is not 0:
                song = info_list.get()
                await self.play_list.put(save_queue.get())
                msg += "{}\n".format(song)

                counter += 1

                msg, counter, how_many = await self.print_songs(msg, message.channel, length, counter, how_many)
        else:
            await self.send_message(channel, "```Queue is currently empty.```")

    async def add(self, channel, link):
        """This function is used to decide what to add to the queue for playing."""
        if link != "":
            """link is an youtube playlist, extract individual songs and add to queue"""
            if link.find("list=") != -1:
                list = None
                playlist = Extract(link)
                list = playlist.check()

                if list is not None:
                    shuffle(list)

                    for song in list:
                        await self.play_list.put(song)
                    await self.bot.send_message(channel, "```I have queued your youtube playlist!```")

                else:
                    await self.bot.send_message(channel, "```Error parsing through list!```")

            elif link.find("http") != -1:
                """link is a single youtube song, just add to queue"""
                await self.play_list.put(link)
                await self.bot.send_message(channel, "```I have queued your song request!```")

            else:
                """if none of the above, link is a youtube query pass to beautifulsoup4 parser to get song and add to queue"""
                link += " lyrics"
                link = parse_yt(link)
                await self.add(channel, link)

        else:
            await self.send_message(channel, "```!play is used to play songs, playlists, youtube playlists or "
                                             "queries!```")
            await self.send_message(channel, "```Usage: !play <url/song/play_list/query>```")

    async def play_music(self, server, channel):
        found = False
        """This function is used to start the music player where channel is the Discord channel that text is sent to."""
        if self.player is None:
            """If the player does not exist, create one. Otherwise move on."""
            while not self.play_list.empty():
                self.play_next_song.clear()
                self.song = await self.play_list.get()

                self.player = await self.voice.create_ytdl_player(self.song, after=self.toggle_next_song)
                self.player.volume = 0.1
                self.player.start()

                info = self.player.title
                msg = ":notes: **Playing:   {}** :notes:\n"

                await self.bot.send_message(channel, msg.format(info))

                """If the recommended songs is set to True, query youtube for the next song and add it to a list to
                prevent repeats. """
                while self.rec_songs and not found:
                    next_url, max = crawl_rec(self.song, max)
                    if self.rec_list.count(next_url) is 0:
                        found = True
                        await self.play_list.put(next_url)
                        self.rec_list.append(next_url)

                found = False

                await self.play_next_song.wait()

    async def rec(self, channel, option):
        if option is not "":
            option = option.strip()
            option = option.lower()

            if option == "on":
                self.rec_songs = True
                await self.bot.send_message(channel, "```Automatic queuing of youtube songs has been turned on!```")

            elif option == "off":
                self.rec_songs = False
                self.rec_list.clear()
                await self.bot.send_message(channel, "```Automatic queuing of youtube songs has been turned off!```")

        else:
            msg = "```The !rec command is used to turn on automatic queueing of youtube songs!  This option is " \
                  "currently {}!```".format(
                self.rec_songs)
            await self.bot.send_message(channel, msg)
