import discord
from discord.ext import commands

class Chat():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self):
        await self.bot.say("Hello!")

def setup(bot):
    bot.add_cog(Chat(bot))
