import discord
from discord.ext import commands
import asyncio
import datetime
import unicodedata
from .utils import checks
import os
from .utils.dataIO import fileIO
pos = {
    "one" : "\U00000031",
    "two" : "\U00000032",
    "three" : "\U00000033",
    "four" : "\U00000034",
    "five" : "\U00000035",
    "six" : "\U00000036",
    "seven" : "\U00000037",
    "eight" : "\U00000038",
    "nine" : "\U00000039",
    "ten" : "\U0001f51f",
    }
default_stats = {"Commands_Used" : 0, "Total_Members" : 0, "Percentage" : 0, "Last_Message": None, "Position": "**Not Ranked Yet!**"}

class Leaderboard:
    """Shows the server leaderboard!
    How It Works
    Your server will be shown based on a percentage
    This percentage is calculated by:
    -Server Members
    -Activeness
    -V9 Commands Used
    Note: Positions will get reset every 1-2 weeks or so
    """
    
    def __init__(self, bot):
        self.bot = bot
        self.leaderboard_data = 'data/leaderboard/settings.json' 

    def time_parse(self, value : int):
        start = int(value.total_seconds())
        hours, remainder = divmod(start, 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        months, days = divmod(days, 30)
        if months:
            kek = '{mn} Months, {d} Days , {h} Hours and {m} Minutes ago'
        else:
            kek = '{d} Days, {h} Hours and {m} Minutes ago'
        return kek.format(mn = months, d = days, h = hours, m = minutes)

    async def on_message(self, message):#This Check is done because some commands do not start with =.
    #So we are going to check how many messages V9 sends.
        data = fileIO(self.leaderboard_data, "load")
        if not message.server.id in data:
            data[message.server.id] = default_stats
            data[message.server.id]["Total_Members"] = len(message.server.members)
            fileIO(self.leaderboard_data, "save", data)
        if message.author.id == message.server.me.id:
            data[message.server.id]["Commands_Used"] += +1
        #self.percentify(server = message.server)
        #self.positionify()
        data[message.server.id]["Last_Message"] = format(message.timestamp, "%d %b %Y at %H:%M UTC TIME")
        data[message.server.id]["Total_Members"] = len(message.server.members)
        fileIO(self.leaderboard_data, "save", data)
    @commands.group(pass_context = True, no_pm = True)
    async def leaderboard(self, ctx):
        """Shows the Leaderboard
        Has Multiple Functions
        do =help leaderboard to know more"""
        server = ctx.message.server
        data = fileIO(self.leaderboard_data, "load")
        if server.id not in data:
            data[server.id] = default_stats
            data[server.id]["Total_Members"] = len(server.members)
            fileIO(self.leaderboard_data, "save", data)
        if ctx.invoked_subcommand is None:
            #self.percentify(server = server.id)
            #self.positionify()
            msg = "**Server Statistics**\n"
            msg += "**Position** : {}\n".format(data[server.id]["Position"])
            msg += "**Total Members** : {}\n".format(data[server.id]["Total_Members"])
            msg += "**Last Message** : {0}\n".format(data[server.id]["Last_Message"])
            msg += "**V9 Commands Used** : {}".format(data[server.id]["Commands_Used"])
            await self.bot.say(msg)
    @leaderboard.command(pass_context=True)
    @checks.is_owner()
    async def setup(self, ctx):
        data = fileIO(self.leaderboard_data, "load")
        for server in self.bot.servers:
            if server.id not in data:
                data[server.id] = default_stats
                data[server.id]["Total_Members"] = len(server.members)
                fileIO(self.leaderboard_data, "save", data)
        await self.bot.reply("Setting up Completed!")

    def percentify(self, server):
        """This creates percentages in all of the server.id's
        a possible 100% out of comparing data"""
        data = fileIO(self.leaderboard_data, "load")
        if not server in data:
            data[server] = default_stats
            data[server]["Total_Members"] = len(server.members)
        member_criteria = 500
        total_mem = int(data[server.id]["Total_Members"])
        mem_percent = round(((total_mem / member_criteria)*100), 1)
        message_criteria = 100
        bot_msgcount = int(data[server.id]["Commands_Used"])
        msg_percent = round(((bot_msgcount/message_criteria)*100),1)
        total_percent = msg_percent + mem_percent
        data[server.id]["Percentage"] = total_percent
        fileIO(self.leaderboard_data, "save", data)
    def positionify(self):
        """Please No Bully :(
        This will create positions based on the checks"""
        data = fileIO(self.leaderboard_data, "load")
        no1 = 0
        no2 = 0
        no3 = 0
        no4 = 0
        no5 = 0
        no6 = 0
        no7 = 0
        no8 = 0
        no9 = 0
        no10 = 0
        highest = 0
        for server in data:
            if int(data[server]["Percentage"]) > highest:
                highest = int(data[server]["Percentage"])
                no1 = data[server]
        no1["Position"] = pos["one"]
        highest = 0
        for server in data:
            if not no1 and int(data[server]["Percentage"]) > highest:
                highest = int(data[server]["Percentage"])
                no2 = data[server]
        no2["Position"] = pos["two"]
        highest = 0
        for server in data:
            if not no1 and not no2 and int(data[server]["Percentage"]) > highest:
                highest = int(data[server]["Percentage"])
                no3 = data[server]
        no3["Position"] = pos["three"]
        highest = 0
        for server in data:
            if not no1 and not no2 and not no3 and int(data[server]["Percentage"]) > highest:
                highest = int(data[server]["Percentage"])
                no4 = data[server]
        no4["Position"] = pos["four"]
        highest = 0
        for server in data:
            if not no1 and not no2 and not no3 and not no4 and int(data[server]["Percentage"]) > highest:
                highest = int(data[server]["Percentage"])
                no5 = data[server]
        no5["Position"] = pos["five"]
        highest = 0
        for server in data:
            if not no1 and not no2 and not no3 and not no4 and not no5 and int(data[server]["Percentage"]) > highest:
                highest = int(data[server]["Percentage"])
                no6 = data[server]
        no6["Position"] = pos["six"]
        highest = 0
        for server in data:
            if not no1 and not no2 and not no3 and not no4 and not no5 and not no6 and int(data[server]["Percentage"]) > highest:
                highest = int(data[server]["Percentage"])
                no7 = data[server]
        no7["Position"] = pos["seven"]
        highest = 0
        for server in data:
            if not no1 and not no2 and not no3 and not no4 and not no5 and not no6 and not no7 and int(data[server]["Percentage"]) > highest:
                highest = int(data[server]["Percentage"])
                no8 = data[server]
        no8["Position"] = pos["eight"]
        highest = 0
        for server in data:
            if not no1 and not no2 and not no3 and not no4 and not no5 and not no6 and not no7 and not no8 and int(data[server]["Percentage"]) > highest:
                highest = int(data[server]["Percentage"])
                no9 = data[server]
        no9["Position"] = pos["nine"]
        highest = 0
        for server in data:
            if not no1 and not no2 and not no3 and not no4 and not no5 and not no6 and not no7 and not no8 and not no9 and int(data[server]["Percentage"]) > highest:
                highest = int(data[server]["Percentage"])
                no10 = data[server]
        no10["Position"] = pos["ten"]
        fileIO(self.leaderboard_data, "save", data)
    async def on_server_join(self, server):
        data = fileIO(self.leaderboard_data, "load")
        data[server.id] = default_stats
        data[server.id]["Total_Members"] = len(server.members)
        fileIO(self.leaderboard_data,"save",data)
    async def on_server_remove(self, server):
        data = fileIO(self.leaderboard_data, "load")
        del data[server.id]
        fileIO(self.leaderboard_data,"save",data)
def check_folders():
    if not os.path.exists("data/leaderboard"):
        print("Creating data/leaderboard folder")
        os.makedirs("data/leaderboard")
def check_files():
    f = "data/leaderboard/settings.json"
    if not fileIO(f, "check"):
        print("Creating leaderboard/settings.json")
        fileIO(f, "save", {})
def setup(bot):
    check_folders()
    check_files()
    n = Leaderboard(bot)
    bot.add_cog(n)

