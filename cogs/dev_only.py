import discord, json
from discord.ext import commands
from player.player import players
from player.item import item_list
from utils import database

class dev_only(commands.Cog):
    '''-developer only-'''
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, cog):
        """reloads the requested cog"""
        try:
            self.bot.unload_extension(f"cogs.{cog}")
            self.bot.load_extension(f"cogs.{cog}")
            await ctx.send(f"`{cog} got reloaded`")
        except Exception as e:
            await ctx.send(f"`{cog} cannot be loaded`")
            raise e

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, cog):
        """unloads the requested cog"""
        try:
            self.bot.unload_extension(f"cogs.{cog}")
            await ctx.send(f"`{cog} got unloaded`")
        except Exception as e:
            await ctx.send(f"`{cog} cannot be unloaded:`")
            raise e

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, cog):
        """loads the requested cog"""
        try:
            self.bot.load_extension(f"cogs.{cog}")
            await ctx.send(f"`{cog} got loaded`")
        except Exception as e:
            await ctx.send(f"`{cog} cannot be loaded:`")
            raise e

    @commands.command()
    @commands.is_owner()
    async def reloadcache(self, ctx):
        players.clear()
        await ctx.message.channel.send("`Cleared. we gucci.`")

    @commands.command()
    @commands.is_owner()
    async def givexp(self, ctx, Player_0: discord.Member, amount=1):
        player = await database.load_player(Player_0.id)
        await player.add_experience(amount,ctx.message.channel)
        database.save_player(player)

    @commands.command()
    @commands.is_owner()
    async def setdesc(self, ctx, *,content: commands.clean_content=None):


        tmp = content.split(" ")

        if len(tmp) < 2:
            await ctx.message.channel.send("`not enough info`")
            return

        item_info = None
        if str(tmp[0]) in item_list:
            item_info = item_list[str(tmp[0])]
        else :
            for key in item_list:
                item = item_list[key]
                if str(tmp[0]).lower() in item["name"].lower():
                    item_info = item
                    break
        
        if item_info == None:
            await ctx.message.channel.send("`not enough info`")
            return

        item_info["description"] = " ".join(tmp[1:])
        with open("player/item_list.json",'w') as open_file:
            json.dump(item_list, open_file, indent=True)
            await ctx.message.channel.send(f"Successfully changed description for **[{item_info['name']}]**.")

    @commands.command()
    @commands.is_owner()
    async def setpicture(self, ctx, *,content: commands.clean_content=None):


        tmp = content.split(" ")

        if len(tmp) < 2:
            await ctx.message.channel.send("`not enough info`")
            return

        item_info = None
        if str(tmp[0]) in item_list:
            item_info = item_list[str(tmp[0])]
        else :
            for key in item_list:
                item = item_list[key]
                if str(tmp[0]).lower() in item["name"].lower():
                    item_info = item
                    break
        
        if item_info == None:
            await ctx.message.channel.send("`not enough info`")
            return

        item_info["thumbnail"] = " ".join(tmp[1:])
        with open("player/item_list.json",'w') as open_file:
            json.dump(item_list, open_file, indent=True)
            await ctx.message.channel.send(f"Successfully changed thumbnail for **[{item_info['name']}]**.")


def setup(bot):
    bot.add_cog(dev_only(bot))