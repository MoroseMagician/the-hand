from discord.ext import commands
from scrape import Scrape
import aiomysql
import discord
import config
import util

bot = commands.Bot(command_prefix = commands.when_mentioned_or(*config.prefixes),
                   description    = config.description,
                   pm_help        = True)

client = discord.Client()

@bot.event
async def on_ready():
    print("Logged in!")
    print("Username: " + bot.user.name)
    print("User ID:  " + bot.user.id)
    await session.connect()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await session.check_message(message)
    await bot.process_commands(message)

if __name__ == "__main__":
    for extension in config.initial_extensions:
        try:
            bot.load_extension(extension)
        except (AttributeError, ImportError) as oops:
            print("Failed to load extension!")
            print("{}: {}".format(type(oops), str(oops)))
    session = Scrape(bot.loop)
    util.make_dir()

bot.run(config.token)
