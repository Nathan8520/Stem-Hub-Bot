from discord.ext.commands import Bot
import discord

intents = discord.Intents(messages=True, guilds=True, members=True)

bot: Bot = Bot(">", intents=intents)

bot.load_extension("exts.information.ping")
bot.load_extension("exts.thank.thank")
bot.load_extension("exts.roles.reactionroles")
#bot.load_extension("exts.roles.autoroles")

bot.run("INSERT TOKEN")

