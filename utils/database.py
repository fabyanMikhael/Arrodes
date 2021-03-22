import json
from player.player import players
from player.player import Player
import utils.mongo
from utils.mongo import PlayerDB

cache = dict()
mongodb_player_data = PlayerDB("Discord-Bot", "Players")

def save_player(player):
    if isinstance(player, Player):
        #print("saved")
        cache[player.id] = player.to_dictionary()
        

async def save_players():
    global cache

    if len(cache) <= 0:
        return

    for index in cache:
        player_data = cache[index]
        if await mongodb_player_data.exists(player_data["_id"]):
            await mongodb_player_data.update(player_data["_id"], player_data)
        else : 
            await mongodb_player_data.add(player_data["_id"], player_data)
    #print(f"# of cached player data: {len(cache)}")
    cache.clear()


async def load_player(id):
    if str(id) in players:
        return players[str(id)]
    if await mongodb_player_data.exists(id):
        player_data = await mongodb_player_data.get(id)
        #print("\nPlayer from database: ",player_data)
        player = Player(
            id=player_data["_id"],
            name=player_data["name"],
            balance=player_data["balance"],
            level=player_data["level"],
            stats=player_data["stats"],
            moves=player_data["moves"],
            equipped_moves=player_data["equipped_moves"],
            inventory=player_data["inventory"],
            misc=player_data["misc"]
            )
        return player
    return Player(id=id)