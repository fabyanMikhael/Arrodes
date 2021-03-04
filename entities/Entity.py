import discord, math, asyncio, random
from Battle import Moves_functions

moves = {"🗡️":0, "🔥":1, "🐓": 2, "<:momo_knife:790743857922179072>":999, "<:kms:790832361931276330>":998, "😐":997, "🚪":996}
id_to_move_emoji = {v: k for k, v in moves.items()}
id_to_move = {0:"Strike", 1:"Fire Ball", 2: "Skip", 999:"Momo's knife", 998:"Self Harm", 997:"Swap", 996: "Flee"}
id_to_energy_move = {0: 3, 1:7, 2: 0, 999: 10, 998: -2, 997:9, 996: 7}

class Entity():
    def __init__(self, name="base-entity", level={"lvl":1, "exp":0, "exp_required":10}, moves=[0,1], stats={"Health":10, "Strength":1, "Speed":1,"Defense":1,"Stamina":1, "Luck": 1, "Intelligence": 1,"Potential":1}):
        self.health = stats['Health']
        self.max_energy = 9 + stats["Stamina"]
        self.energy = 9 + stats["Stamina"]
        self.name = f"{name}"
        self.id = 0
        self.level = level
        self.dmg = stats["Strength"]
        self.stats = stats
        self.moves = moves
        self.equipped_moves = moves
        self.icon = "https://cdn.discordapp.com/attachments/694352452446584975/790037826917629982/unknown.png"
    

    async def death(self, message, killer, game):
        await game.Death(message.channel, killer, self)

    async def take_damage(self, dmg, game, player_number, move=None):
        damage_in_bars = math.floor((dmg/self.stats["Health"]) * 10)
        player1_health = math.ceil(((game.players[0].health)/game.players[0].stats["Health"]) * 10)
        player2_health = math.ceil(((game.players[1].health)/game.players[1].stats["Health"]) * 10)
        self.health = max(self.health - dmg, 0)
        await game.updateEmbed(int(not player_number) * damage_in_bars, player_number * damage_in_bars, player1_health, player2_health, move)


    async def prepare(self, player_number, game):
        #await game.message.add_reaction("⚔️")
        self.energy = min((self.energy + 1), self.max_energy)
        await asyncio.sleep(1.6)
        await self.turn(player_number,game)
        if await game.check_win_condition(): return
        game.turn = int(not game.turn)
        await game.players[game.turn].prepare(game.turn, game)


    async def turn(self, player_number, game, reaction=None):
        move = random.choice(self.get_allowed_moves())
        await self.use_move(move, player_number, game)

    async def use_move(self, move, player_number, game):
        self.energy -= id_to_energy_move[move]
        function_name = Moves_functions.__dict__[f"move_{move}"]
        await asyncio.sleep(0.1)
        await function_name(self, move, player_number, game)

    async def rewards(self, game, player_number):
        pass

    def get_allowed_moves(self):
        result = []
        for move in self.equipped_moves:
            if self.energy >= id_to_energy_move[move]:
                result.append(move)
        return result + [2]

    def get_energy(self):
        return math.floor((self.energy/self.max_energy) * 10)

    def equipped_moves_to_str(self):
        return f"**[{self.name}] is deciding on a move to use....**<a:loading:794672829202300939>"