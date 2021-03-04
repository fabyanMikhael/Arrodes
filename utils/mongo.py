import os
import pymongo
import motor.motor_asyncio

MONGOURI = os.environ["MONGOURI"]
# add the MONGOURI to ur .env


class PlayerDB:
    def __init__(self, collection_name, document_name):
        self.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(MONGOURI))
        self.collection = self.mongo[collection_name]
        self.db = self.collection[document_name]

    # -- Pointer Methods --
    async def get(self, member_id):
        """
        Points to self.get_player
        """
        return await self.get_player(member_id)

    async def add(self, member_id, player_data):
        """
        Points to self.upsert_player
        """
        await self.upsert_player(member_id, player_data)

    async def update(self, member_id, updated_player):
        """
        Points to self.update_player
        """
        await self.update_player(member_id, updated_player)

    async def exists(self, member_id):
        """
        Points to self.player_exists
        """
        return await self.player_exists(member_id)

    async def remove(self, member_id):
        """
        Points to self.delete_player
        """
        await self.delete_player(member_id)

    # -- Actual Methods --
    async def get_player(self, member_id):
        """
        Returns a player object with the given member_id
        """
        return await self.db.find_one({"_id": int(member_id)})

    async def upsert_player(self, member_id, player_data):
        """
        Upserts a player object into the database
        """
        player = player_data
        player["_id"] = member_id
        try:
            await self.db.insert_one(player)
        except pymongo.errors.DuplicateKeyError:
            return

    async def update_player(self, member_id, updated_player):
        """
        Updates a player object in the database
        """
        updated_player["_id"] = member_id

        await self.db.update_one(
            {"_id": member_id}, {"$set": updated_player},
        )

    async def player_exists(self, member_id):
        """
        Checks if a player exists in the database with the given member_id
        Returns a boolean value on the existence of the player
        """
        player = await self.get_player(member_id)
        return True if player is not None else False

    async def delete_player(self, member_id):
        """
        Deletes the player found with the given member_id
        """
        if not await self.get_player(member_id):
            return

        await self.db.delete_one({"_id": member_id})


# used only for testing, comment out everything below
# import asyncio


# async def bruh():
#     test = PlayerStuff("games", "currency")
#     # await test.add("fools_id", "foolmoment")
#     stats = {
#         "max_health": 10,
#         "name": "Fool BRuh",
#         "level": {"lvl": 900, "exp": 40, "exp_required": 170},
#         "dmg": 10,
#         "moves": [0, 1],
#         "equipped_moves": [0, 1],
#         "inventory": [],
#         "balance": 0,
#         "stats": {},
#         "misc": {},
#     }
#     await test.update(member_id="fools_id", updated_player=stats)


# loop = asyncio.get_event_loop()
# loop.run_until_complete(bruh())
