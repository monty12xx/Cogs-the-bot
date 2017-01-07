    @commands.command(pass_context=True, no_pm=True)
    async def serverinfo(self, ctx):
        """Shows server's informations"""
        server = ctx.message.server
        online = len([m.status for m in server.members
                      if m.status == discord.Status.online or
                      m.status == discord.Status.idle])
        total_users = len(server.members)
        text_channels = len([x for x in server.channels
                             if x.type == discord.ChannelType.text])
        voice_channels = len(server.channels) - text_channels
        passed = (ctx.message.timestamp - server.created_at).days
        created_at = ("Created on {} ({} days ago!)"
                      "".format(server.created_at.strftime("%d %b %Y %H:%M"),
                                passed))

        colour = ''.join([randchoice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        data = discord.Embed(
            description="Server ID: " + server.id,
            colour=discord.Colour(value=colour))
        data.add_field(name="Region", value=str(server.region))
        data.add_field(name="Users", value="{}/{}".format(online, total_users))
        data.add_field(name="Text Channels", value=text_channels)
        data.add_field(name="Voice Channels", value=voice_channels)
        data.add_field(name="Roles", value=len(server.roles))
        data.add_field(name="Owner", value=str(server.owner))
        data.set_footer(text=created_at)

        if server.icon_url:
            data.set_author(name=server.name, url=server.icon_url)
            data.set_thumbnail(url=server.icon_url)
        else:
            data.set_author(name=server.name)
            if len(server.emojis) > 0:
                a = ''
                emotelist = list(e for e in server.emojis if not e.managed)
                for x in range(7):
                    randemote = randchoice([k for k in emotelist])
                    a += '<:{0.name}:{0.id}>  '.format(randemote)
                    emotelist = emotelist.remove(randemote)
                emoji = a
                if len(server.emojis) > 30:
                    em_field = "Showing 7 random emojis from {} Total Emojis\n{}".format(len(server.emojis), emoji)
                else:
                    em_field = "{} Emojis\n{}".format(len(server.emojis), emoji)
                data.add_field(name = "Server Emotes", value = em_field)
            else:
                data.add_field(name = "Server Emotes", value = "**No Server Emojis**")         

        try:
            await self.bot.say(embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")
