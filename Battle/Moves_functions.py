import asyncio, discord

async def move_0(self, move, player_number, game):
    await game.players[int(not player_number)].take_damage(self.stats['Strength'], game, int(not player_number), f"**{self.name}** used **[Strike]** 🔻{self.stats['Strength']} Damage!")

async def move_1(self, move, player_number, game):
    await game.players[int(not player_number)].take_damage(self.stats['Strength'] * 2, game, int(not player_number), f"**{self.name}** used **[Fire Ball]** 🔻{self.stats['Strength'] * 2} Damage!")

async def move_2(self, move, player_number, game):
    await game.players[int(not player_number)].take_damage(0, game, int(not player_number), f"**{self.name}** has decided to skip their turn...")

async def move_999(self, move, player_number, game):
    await game.players[int(not player_number)].take_damage(self.stats['Strength'] * 10000, game, int(not player_number), f"**{self.name}** used **[Momo Knife]** 🔻{self.stats['Strength'] * 10000} Damage!")

async def move_998(self, move, player_number, game):
    await game.players[int(player_number)].take_damage(10, game, player_number, f"**{self.name}** used **[Self Harm]** 🔻10 Damage!")

async def move_997(self, move, player_number, game):
    temp_health = game.players[0].health
    temp_maxhealth = game.players[0].stats['Health']
    temp_dmg = game.players[0].dmg
    temp_moves = game.players[0].equipped_moves.copy()

    game.players[0].health = game.players[1].health
    game.players[0].stats['Health'] = game.players[1].stats['Health']
    game.players[0].dmg = game.players[1].dmg
    game.players[0].equipped_moves = game.players[1].equipped_moves.copy()

    game.players[1].health = temp_health
    game.players[1].stats['Health'] = temp_maxhealth
    game.players[1].dmg = temp_dmg
    game.players[1].equipped_moves = temp_moves

    await game.players[int(not player_number)].take_damage(0, game, int(not player_number), f"**{self.name}** used **[Swap]** Health, Damage, and moves been swapped!")
    await asyncio.sleep(1.5)

async def move_996(self, move, player_number, game):
    await asyncio.sleep(1)
    embed=discord.Embed(title="<a:dark_red_flame:791084503317741589>Battle Results<a:dark_red_flame:791084503317741589>", color=0x23162a)
        
    embed.set_author(name=f"[Fight] - Ended") 
        
    embed.add_field(name="<:blank:794678298026180608>",value=f"**[{game.players[player_number].name}]** has fled!", inline=False)
    
    await game.message.clear_reactions()
        
    await game.message.edit(embed=embed) 
    
    await game.End_Game()