from discord.ext import commands

import discord
import discord.utils

class Invite(object):
	def __init__(self, bot):
		self.bot = bot
	@commands.command()
	async def invite(self):
		"""Returns the bots invite link and help server."""
		client_id = await self.bot.application_info()
		link = "https://discordapp.com/oauth2/authorize?client_id=234179578229293057&scope=bot&permissions=536083519"
		_message = "You can invite me using this link: {0}"
		await self.bot.say(_message.format(link))

def setup(bot):
	bot.add_cog(Invite(bot))
