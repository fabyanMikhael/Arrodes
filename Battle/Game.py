import discord, asyncio, math
from utils import database
from entities.Entity import moves
from player.item import item_icon_to_name

games = dict()

bar ={      "start1": "<:start:790075380039942164>",
            "start2": "<:start2:790076661039104020>",
            "start3": "<:start3:790077352419524609>",
            "middle1": "<:middle:790075379606880277>",
            "middle2": "<:middle2:790076660849442817>",
            "middle3": "<:middle3:790077352650342410>",
            "end1": "<:end:790075379996950558>",
            "end2": "<:end2:790076661197570049>",
            "end3": "<:end3:790077352633434132>"}

def GetHealthBar(dmg_=0, health_=5):
    health = min(health_,10)
    health = max(health, 0)
    dmg = min(health, dmg_)
    result = ""
    expected_health = (health - dmg)
    if expected_health  >= 1: 
        result += bar["start1"]
        if expected_health >= 10:
            result += bar["middle1"] * 8 + bar["end1"]
        elif health >= 10:
            result += bar["middle1"] * (9-dmg) + bar["middle2"] * (dmg - 1) + bar["end2"]
        else:
            result += bar["middle1"] * (expected_health - 1) + bar["middle2"] * (dmg) + bar["middle3"] * (9 - health) + bar["end3"]
    elif expected_health <= 0:
        result += bar["start2"] + bar["middle2"] * (dmg - 1) + bar["middle3"] * (9 - dmg) + bar["end3"]
    else:
        result += bar["start3"] + bar["middle3"] * 8 + bar["end3"]
    return result

def GetEnergyBar(energy=10):

    if energy == 10:
        return bar["start1"] + bar["middle1"] * 8 + bar["end1"]

    if energy >= 1:
        return bar["start1"] + bar["middle1"] * (energy - 1) + bar["middle3"] * (10 - energy - 1) + bar["end3"]

    return bar["start3"] + bar["middle3"] * 8 + bar["end3"]

class Game():

    def __init__(self, Player1, Player2, channel):
        Player1.health = Player1.stats['Health']
        Player1.energy = Player1.max_energy
        Player1.in_game = True

        Player2.health = Player2.stats['Health']
        Player2.energy = Player2.max_energy
        Player2.in_game = True

        self.players = [Player1, Player2]
        self.turn = 0
        self.message = None
        self.id = None
        self.has_ended = False
        self.tmp = 0

    async def create(self, channel):
        #embed=discord.Embed(title=self.players[1].name + " - lvl." + str(self.players[1].level["lvl"]), color=0xa43232)
        embed=discord.Embed(color=0x00aa00)
        #embed.set_footer(text=f"Requested by {self.player}", icon_url=self.player.avatar_url,)
        embed.set_thumbnail(url=self.players[1].icon)
        embed.set_author(name=f"[Fight] {self.players[self.turn].name}'s turn",icon_url=self.players[1].icon) 


        player1_healthText = GetHealthBar(0,10) + f" - ❤️ {self.players[1].health}/{self.players[1].stats['Health']}"
        player1_EnergyText = f" \nEnergy:\n {GetEnergyBar(self.players[1].get_energy())} - ⚡ {self.players[1].energy}/{self.players[1].max_energy}"

        player0_healthText = GetHealthBar(0,10) + f" - ❤️ {self.players[0].health}/{self.players[0].stats['Health']}"
        player0_EnergyText = f" \nEnergy:\n {GetEnergyBar(self.players[0].get_energy())} - ⚡ {self.players[0].energy}/{self.players[0].max_energy}"

        available_moves = "\n\n" + self.players[0].equipped_moves_to_str() + "\n**[<:backpack:796160766486511637> Inventory]**"

        embed.add_field(name=f"**[{self.players[1].name} lvl.{self.players[1].level['lvl']}]'s** Health: ", value=(player1_healthText + player1_EnergyText), inline=False)
        embed.add_field(name=f"**[{self.players[0].name} lvl.{self.players[0].level['lvl']}]'s** Health: ", value=(player0_healthText + player0_EnergyText + available_moves), inline=False)
        msg = await channel.send(embed=embed)
        self.id = msg.id
        self.message = msg
        await self.players[0].prepare(0,self)
        games[self.id] = self
        await asyncio.sleep(0.2)



    async def reaction_event(self, reaction, member):
        if self.has_ended:
            await self.message.clear_reactions() 
            return

        if (self.players[0].id == member.id and self.turn == 0) or (self.players[1].id == member.id and self.turn == 1):

            if await self.check_win_condition(): return


            if await self.check_item_use(reaction,member): return

            if not str(reaction.emoji) in moves: return
            if not (moves[str(reaction.emoji)] in self.players[self.turn].get_allowed_moves()): return
            await self.players[self.turn].turn(self.turn, self, reaction)

            await self.message.clear_reactions()

            if await self.check_win_condition(): return

            self.turn = int(not self.turn)


            await asyncio.sleep(0.3)
            await self.players[self.turn].prepare(self.turn, self)
        
            if await self.check_win_condition(): return

        else:
            await reaction.message.remove_reaction(reaction,member)

    async def check_item_use(self, reaction, member):

        if str(reaction.emoji) == '<:backpack:796160766486511637>':
            text = '\n\n**[Inventory]**\n'
            
            for item in self.players[self.turn].equipped_items:
                text += f"\n**[{item.icon} {item.name} x{item.amount}]**"

            player1_health = math.ceil(((self.players[0].health)/self.players[0].stats['Health']) * 10)
            player2_health = math.ceil(((self.players[1].health)/self.players[1].stats['Health']) * 10)

            await self.updateEmbed(0,0,player1_health,player2_health,' ',text, self.turn)
            await self.message.clear_reactions()

            for item in self.players[self.turn].equipped_items:
                await self.message.add_reaction(item.icon)

            await self.message.add_reaction("↩️")
            return True
        
        if str(reaction.emoji) == '↩️':
            await self.message.clear_reactions()
            player1_health = math.ceil(((self.players[0].health)/self.players[0].stats['Health']) * 10)
            player2_health = math.ceil(((self.players[1].health)/self.players[1].stats['Health']) * 10)
            await self.updateEmbed(0,0,player1_health,player2_health,turn=self.turn)
            await self.players[self.turn].prepare(self.turn, self, refill_energy=False)
            return True
        
        if str(reaction.emoji) in item_icon_to_name:
            item_id = item_icon_to_name[str(reaction.emoji)]
            if self.players[self.turn].hasItem(item_id):


                await self.message.clear_reactions()
                txt = self.players[self.turn].useItem(item_id, self)
                player1_health = math.ceil(((self.players[0].health)/self.players[0].stats['Health']) * 10)
                player2_health = math.ceil(((self.players[1].health)/self.players[1].stats['Health']) * 10)
                await self.updateEmbed(0,0,player1_health,player2_health,turn=self.turn, move=txt)
                await self.players[self.turn].prepare(self.turn, self, refill_energy=False)
                return True
        
        
        

    

    async def check_win_condition(self):
        if self.has_ended: return True

        if self.players[0].health <= 0:
            await self.Death(self.message.channel, self.players[1], self.players[0])
            await self.players[1].rewards(self, 1)
            database.save_player(self.players[1])
            await self.message.clear_reactions()
            return True

        if self.players[1].health <= 0:
            await self.Death(self.message.channel, self.players[0], self.players[1])
            await self.players[0].rewards(self, 0)
            database.save_player(self.players[0])
            await self.message.clear_reactions()
            return True

        return False

    async def updateEmbed(self, damage_1=0, damage_2=0, health_1=10, health_2=10, move=None, extra_info=None, turn=None):
        print("move: ", move)
        healthbar_1 = GetHealthBar(damage_1, health_1)
        healthbar_2 = GetHealthBar(damage_2, health_2)
        if turn == None:
            turn = int(not self.turn)
        
        #embed=discord.Embed(title=self.players[1].name + " - lvl." + str(self.players[1].level["lvl"]), color=0xa43232)
        
        embed = None
        if self.turn == 1: embed=discord.Embed(color=0x00aa00)
        else: embed=discord.Embed(color=0x0003aa)
        
        embed.set_thumbnail(url=self.players[1].icon)
        
        embed.set_author(name=f"[Fight] {self.players[turn].name}'s turn",icon_url=self.players[1].icon) 

        player1_healthText = healthbar_2 + f" - ❤️ {self.players[1].health}/{self.players[1].stats['Health']}"
        player1_EnergyText = f" \nEnergy:\n {GetEnergyBar(self.players[1].get_energy())} - ⚡ {self.players[1].energy}/{self.players[1].max_energy}"

        player0_healthText = healthbar_1 + f" - ❤️ {self.players[0].health}/{self.players[0].stats['Health']}"
        player0_EnergyText = f" \nEnergy:\n {GetEnergyBar(self.players[0].get_energy())} - ⚡ {self.players[0].energy}/{self.players[0].max_energy}"

        if move == None: move = ""
        
        embed.add_field(name=f"**[{self.players[1].name} - lvl.{self.players[1].level['lvl']}]'s** Health: ", value=(player1_healthText + player1_EnergyText + f"\n\n {move}\n"), inline=False)
        
        available_moves = "\n\n" + self.players[turn].equipped_moves_to_str() + "\n**[<:backpack:796160766486511637> Inventory]**"
        
        # Temporary, used for swapping the last bit of text with inventory stuff instead
        if extra_info != None: available_moves = str(extra_info)
    
        f"\n\n**[{self.players[0].name} - lvl.{self.players[0].level['lvl']}]'s** Health: "

        embed.add_field(name=f"\n\n**[{self.players[0].name} - lvl.{self.players[0].level['lvl']}]'s** Health: ", value=(player0_healthText + player0_EnergyText + available_moves), inline=False)
        
        await self.message.edit(embed=embed) 

    async def Death(self, channel, killer, victim):
        await asyncio.sleep(2)
        embed=discord.Embed(title="<a:dark_red_flame:791084503317741589>Battle Results<a:dark_red_flame:791084503317741589>", color=0x23162a)
        
        embed.set_author(name=f"[Fight] - Ended") 
        
        embed.add_field(name=f"[{victim.name} - lvl.{victim.level['lvl']}] has died!", value=(f"Killed by: [{killer.name} - lvl.{killer.level['lvl']}]"), inline=False)
        
        await self.message.clear_reactions()
        
        await self.message.edit(embed=embed) 
        
        await self.End_Game()

        return

    async def End_Game(self):
        self.has_ended = True

        for p in self.players:
            p.in_game = False

        games.pop(self.id, None)
        return
