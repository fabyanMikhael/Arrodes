import discord, asyncio
from discord.ext import commands
from Battle.Game import games

class pve(commands.Cog):
    '''contains all the pve commands'''
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, member):
        if member == self.bot.user:
            return
        if reaction.message.id in games:
            await asyncio.sleep(0.2)
            
            game = games[reaction.message.id]
            await asyncio.sleep(0.1)
            await game.reaction_event(reaction, member)

def setup(bot):
    bot.add_cog(pve(bot))