from datetime import datetime

from discord import Embed, TextChannel
from discord.ext.commands import Bot, Cog, Context, command
import discord.ext.commands as commands
from discord.utils import get
from discord.ext import tasks
import discord

import exts.thank.dbs as dbs

class Auto(Cog):

    def __init__(self, bot: Bot):
        self.bot: Bot = bot
        self.roles = [921796523518468107]

    @Cog.listener()
    async def on_member_join(self, member: discord.Member):
        for id in self.roles:
            role = member.guild.get_role(id)
            await member.add_roles(role)


def setup(bot: Bot):
    bot.add_cog(Auto(bot))