import discord, asyncio
from discord.ext import tasks, commands
from utils import database

class scheduled_saving(commands.Cog):
    '''periodically saves cached player data'''
    def __init__(self, bot):
        self.bot = bot
        self.printer.start()

    def cog_unload(self):
        self.printer.cancel()

    @tasks.loop(seconds=5.0)
    async def printer(self):
        #print("Saving cached data...")
        await database.save_players()

def setup(bot):
    bot.add_cog(scheduled_saving(bot))