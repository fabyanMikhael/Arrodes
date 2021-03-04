import discord, random, entities
from entities.Entity import Entity
from Battle.Game import Game, games
from player.player import Player
from discord.ext import commands
from utils import database



#Temporary----
enemy_presets = []
with open("example.txt", "r") as a_file:
  for line in a_file:
    if "#" in line: continue
    enemy_presets.append(line.replace("\n","").split(" "))
    print(f"loaded enemy #{len(enemy_presets)}: {enemy_presets[-1][0]}")
#Temporary----



class pvp(commands.Cog):
    '''contains all the pvp commands'''
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def attack(self, ctx, victim: discord.Member):
        ''': wit da shi'''
        #human = Entity(10000, str(victim.name), dmg=100)
        player1 = await database.load_player(ctx.author.id)
        player1.name = ctx.author.name
        player2 = await database.load_player(victim.id)
        player2.name = victim.name

        game = Game(player1,player2,ctx.message.channel)
        await game.create(ctx.message.channel)
        
        await ctx.message.delete()

    @commands.command()
    async def fight(self, ctx):
        ''': wit da shi'''

        choice = random.choice(enemy_presets)
        enemy = Entity(choice[0])
        enemy.level['lvl'] = int(choice[3])
        
        p = await database.load_player(ctx.author.id)
        p.name = ctx.author.name
        
        game = Game(p,enemy,ctx.message.channel)
        await game.create(ctx.message.channel)
            
        await ctx.message.delete()

    @commands.command()
    @commands.is_owner()
    async def testing(self, ctx):
        ''': wit da shi'''

        choice = random.choice(enemy_presets)
        enemy = Entity(choice[0])
        enemy.level['lvl'] = int(choice[3])

        choice = random.choice(enemy_presets)
        enemy2 = Entity(choice[0])
        enemy2.level['lvl'] = int(choice[3])

        game = Game(enemy, enemy2,ctx.message.channel)
        await game.create(ctx.message.channel)
            
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(pvp(bot))
