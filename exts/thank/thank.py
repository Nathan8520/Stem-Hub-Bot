from datetime import datetime

from discord import Embed, TextChannel
from discord.ext.commands import Bot, Cog, Context, command
import discord.ext.commands as commands
from discord.utils import get
from discord.ext import tasks

import exts.thank.dbs as dbs

class Thank(Cog):

    def __init__(self, bot: Bot):
        self.bot: Bot = bot

        self.updateLeaderboard.start()

    @command()
    async def unthank(self, ctx: Context, user) -> None:
        mod = get(ctx.guild.roles, id=903585824296288278)
        admin = get(ctx.guild.roles, id=903585664325529640)

        if not (mod in ctx.author.roles or admin in ctx.author.roles):
            return

        if user [0] == '<':
            user = user [3:-1]
        user = int(user)

        user = get(ctx.guild.members, id=user)

        if user is None:
            embed = Embed(title="", description="This is not a vaild member", color=0xaa0000)
            await ctx.send(embed=embed)
            return

        count = dbs.getThanks(user.id)

        dbs.setThanks(user.id, max(0, count [0]-1), max(0, count [1]-1))

        embed = Embed(title="", description=f"{ctx.author.mention} You have just unthanked {user.mention}!\nThey now have {max(0, count [0]-1)} total thanks!", color=0xbb0000)
        await ctx.send(embed=embed)

    @command()
    async def thanks(self, ctx: Context, user="None") -> None:
        try:
            if user [0] == '<':
                user = user [3:-1]
            user = int(user)

            user = get(ctx.guild.members, id=user)
        except:
            user = ctx.author

        count = dbs.getThanks(user.id)
        rank = dbs.getRank(user.id)
        rank = str(rank) + (["st","nd","rd","th"][min(4, rank%10)-1])

        embed = Embed(title=f"Thanks {user.display_name}", description="", color=0x00aa00)
        embed.add_field(name="Total", value=count [0], inline=True)
        #embed.add_field(name="Weekly", value=count [1], inline=True)
        embed.set_footer(text=rank)

        await ctx.send(embed=embed)

    @command()
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def thank(self, ctx: Context, user) -> None:
        if user [0] == '<':
            user = user [3:-1]
        user = int(user)

        user = get(ctx.guild.members, id=user)

        if user is None:
            embed = Embed(title="", description="This is not a vaild member", color=0xaa0000)
            await ctx.send(embed=embed)
            return
        if user.id == ctx.author.id:
            embed = Embed(title="", description="You cant thank yourself", color=0x0aa0000)
            await ctx.send(embed=embed)
            return

        count = dbs.getThanks(user.id)

        dbs.setThanks(user.id, count [0]+1, count [1]+1)

        embed = Embed(title="", description=f"{ctx.author.mention} You have just thanked {user.mention}!\nThey now have {count [0]+1} total thanks!", color=0x00aaaa)
        await ctx.send(embed=embed)

    @thank.error
    async def thank_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = Embed(title=f"", description=f"You can only use this command once every 10mins!\nTry again in {int(error.retry_after/60)}mins{int(error.retry_after)%60}s.",
                               color=0xaaaa00)
            await ctx.send(embed=embed)

    @command()
    async def createLeaderboard(self, ctx: Context) -> None:
        await ctx.send("Temp message")

    @tasks.loop(seconds=120)
    async def updateLeaderboard(self):
        channel: TextChannel = await self.bot.fetch_channel(904402752334090280)
        message = await channel.fetch_message(904403511318569040)

        users = dbs.getTop()

        desc = ""

        for x in range(10):
            if x >= len(users):
                break

            desc += f"{x+1}) <@{users [x][0]}>                                      {users [x][1]}\n"

        embed = Embed(title="Tutor Leaderboard", description=desc, color=0x00aaaa)

        await message.edit(content="", embed=embed)



def setup(bot: Bot):
    bot.add_cog(Thank(bot))