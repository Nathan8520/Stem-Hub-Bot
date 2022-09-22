from datetime import datetime

from discord import Embed
from discord.ext.commands import Bot, Cog, Context, Command


class Ping(Cog):

    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    @Command
    async def ping(self, ctx: Context):
        current_time: datetime = datetime.utcnow()
        message_time: datetime = ctx.message.created_at
        processing_time: float = (current_time - message_time).total_seconds() * 1000
        pretty_processing_time: str = f"{processing_time:.3f} ms"

        bot_latency: float = self.bot.latency
        pretty_bot_latency: str = f"{bot_latency * 1000:.3f} ms"

        embed: Embed = Embed(title="Pong!", colour=0x00ff00)
        embed.set_footer(text=f"Requested by {ctx.author.display_name}#{ctx.author.discriminator}")
        embed.timestamp = current_time

        descriptions: tuple[str, str] = ("Command Processing Time", "Discord API Latency")

        for desc, latency in zip(descriptions, (pretty_processing_time, pretty_bot_latency)):
            embed.add_field(name=desc, value=latency, inline=False)

        await ctx.send(embed=embed)

        return


def setup(bot: Bot):
    bot.add_cog(Ping(bot))
