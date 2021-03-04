from entities.Entity import Entity
from entities.Entity import moves, id_to_move_emoji, id_to_move, id_to_energy_move
from player.item import item
import discord, asyncio, json

players = dict()


class Player(Entity):
    def __init__(self, name="base-player", level={"lvl":1, "exp":0, "exp_required":10}, id=0, balance=0, moves = [0,1,996], inventory=dict(), stats={"Health":10, "Strength": 1, "Speed":1,"Defense":1,"Stamina":1, "Luck": 1, "Intelligence": 1,"Potential":1}, misc={"Upgrade Points": 0}, equipped_moves=[0,1,996], equipped_items=[]):
        super().__init__( name, level.copy(), moves.copy(), stats=stats.copy())
        self.id = id
        self.equipped_moves=equipped_moves.copy()
        self.inventory = self.dictionary_to_items(inventory)
        self.balance = balance
        self.misc = misc.copy()
        self.equipped_items = self.inventory
        players[str(self.id)] = self
        print("Player creating: ",str(self.id))

    def dictionary_to_items(self, dictionary):
        if dictionary == None:
            return []
        items = []
        for id in dictionary:
            items.append(item(int(dictionary[id]),id=int(id)))
        return items


    async def prepare(self, player_number, game, refill_energy=True):
        if game.has_ended: return
        for move_id in self.get_allowed_moves():
            await game.message.add_reaction(id_to_move_emoji[move_id])
        
        await game.message.add_reaction('<:backpack:796160766486511637>')

        if refill_energy: self.energy = min((self.energy + 1), self.max_energy)

    async def turn(self, player_number, game, reaction=None):
        if str(reaction.emoji) in moves:
            move = moves[str(reaction.emoji)]
            if move in self.get_allowed_moves(): await self.use_move(move, player_number, game)


    async def rewards(self, game, player_number):
        if game.tmp == 1:
            return
        game.tmp = 1;
        exp_gain = game.players[int(not player_number)].level["lvl"] * 2 
        self.add_item(0,10)
        await self.add_experience(exp_gain, game.message.channel)

    def add_item(self, id, amount):
        for Items in self.inventory:
            if int(Items.id) == int(id):
                Items.amount += amount
                return
        self.inventory.append(item(amount,id=id))

    async def add_experience(self, amount, channel):
        exp_gain = amount
        exp_gain = round((exp_gain) * (1 + ((self.stats["Potential"]/2) * 0.1)), 1)
        self.level["exp"] += exp_gain

        # TEMPORARY
        msgs = await self.check_for_level_up()
        text1 = msgs[:int(len(msgs)/2)]
        text2 = msgs[int(len(msgs)/2):]
        if len(text1) > 0: await channel.send(content="".join(text1))
        if len(text2) > 0: await channel.send(content="\n"+"".join(text2))

        # TEMPORARY

        embed=discord.Embed(title=self.name + " - lvl." + str(self.level["lvl"]), color=0xa43232)
        #embed.set_thumbnail(url=self.icon)
        embed.set_author(name="|Battle Rewards|",icon_url="https://cdn.discordapp.com/attachments/694352452446584975/790037826917629982/unknown.png") 
        embed.add_field(name="__You obtained:__", value=f"\n**• {exp_gain}+ exp**\n• 10+ 🍎", inline=False)
        await channel.send(embed=embed)

    async def check_for_level_up(self):
        if (self.level["exp"] >= self.level["exp_required"]):
            self.level["exp"] -= self.level["exp_required"]
            self.level["exp_required"] += 10
            self.level["lvl"] += 1
            self.misc["Upgrade Points"] += 2
            text = f"\n<a:dark_red_flame:791084503317741589>**[{self.name}] You have leveled up!<a:dark_red_flame:791084503317741589>\n<a:dark_red_flame:791084503317741589> Current level: {self.level['lvl']}**<a:dark_red_flame:791084503317741589>\n"
            return [text] + await self.check_for_level_up()
        return []

    def equipped_moves_to_str(self):
        result = "Available Moves: \n"
        temporary = self.get_allowed_moves()
        for move_id in temporary:
            result += f"   **[{id_to_move_emoji[move_id]} {id_to_move[move_id]} : ⚡{id_to_energy_move[move_id]}]**\n"
        return result

    def to_dictionary(self):
        result = dict()
        result["_id"] = self.id
        result["name"] = self.name
        result["balance"] = self.balance
        result["level"] = self.level
        result["stats"] = self.stats
        result["moves"] = self.moves
        result["equipped_moves"] = self.equipped_moves
        result["inventory"] = self.items_to_dictionary(self.inventory)
        result["misc"] = self.misc
        return result

    def items_to_dictionary(self, items):
        result = dict()
        for item in items:
            result[str(item.id)] = item.amount
        return result
        
    def hasItem(self, item_id):
        for item in self.inventory:
            if int(item_id) == int(item.id):
                return True
        return False

    def useItem(self, item_id, game):
        for Item in self.inventory:
            
            if int(Item.id) == int(item_id):
                tmp = Item.__use__(self, game)
                if Item.amount <= 0:
                    self.inventory.remove(Item)
                return tmp