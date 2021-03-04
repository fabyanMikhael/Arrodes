import discord, asyncio, math
from player.player import players
from discord.ext import commands
from entities.Entity import id_to_move, id_to_move_emoji
from player.item import item_list
from utils import database


stats_to_emote = {"health" : "❤️", "strength" :"⚔️","luck": "🎲", "stamina":"🔋", "defense":"🛡️", "speed":"👟", "intelligence":"🧠", "potential":"<:LightningBolt:791545871753150494>"}

class profile(commands.Cog):
    '''contains all the profile commands'''
    def __init__(self, bot):
        self.bot = bot

    def get_experience_bar(self, exp, required):
        to_bar = math.floor((exp/required) * 10)
        return to_bar * "🟩" + (10 - to_bar) * "⬛"


    @commands.command()
    async def level(self, ctx):
        ''': shows the user's current level and progress'''
        embed=discord.Embed(title="<a:green_flame:791074893449134080>level Progress<a:green_flame:791074893449134080>", color=0xa43232)
       
        embed.set_author(name=f"[{ctx.message.author.name}]",icon_url=ctx.message.author.avatar_url) 
      
        player1 = await database.load_player(ctx.message.author.id)
        player1.name = ctx.message.author.name
        
        text = f"\nExperience: {player1.level['exp']}/{player1.level['exp_required']}"

        exp_gain = round(1 + ((player1.stats["Potential"]/2) * 0.1), 1) - 0.1

        embed.add_field(name=f" Current Level: [{player1.level['lvl']}] - {exp_gain}x exp gain [ **{player1.stats['Potential']}** <:LightningBolt:791545871753150494> ]", value=f"{self.get_experience_bar(player1.level['exp'],player1.level['exp_required'])}"+text, inline=False)

        #embed.set_thumbnail(url=player1.icon)

        await ctx.message.channel.send(embed=embed)

    @commands.command(aliases=["Stats", "profile"])
    async def stats(self, ctx):
        ''': shows the user's current level and progress'''
        embed=discord.Embed(title="<a:green_flame:791074893449134080>Stats<a:green_flame:791074893449134080>", color=0xa43232)
       
        embed.set_author(name=f"[Profile]",icon_url=ctx.message.author.avatar_url) 
      
        player1 = await database.load_player(ctx.message.author.id)
        player1.name = ctx.author.name
        
        text = f"\n"
        for key in player1.stats:
            text += f"\n**{key}**: {player1.stats[key]} "
            if key.lower() in stats_to_emote:
                text += stats_to_emote[key.lower()]
    
        text += f"\n\n**Upgrade Points:** {player1.misc['Upgrade Points']}  <:plus:795070844745154590>"

        text += "\n\n`[Moves unlocked]` "
        for move in player1.moves:
            text += f"\n**[{id_to_move[int(move)]} {id_to_move_emoji[int(move)]}]**"

        embed.add_field(name=f"\n\n`[{ctx.message.author.name} - lvl.{player1.level['lvl']}]`", value=text, inline=False)

        #embed.set_thumbnail(url=player1.icon)

        await ctx.message.channel.send(embed=embed)

    @commands.command()
    async def moves(self, ctx):
        ''': shows the user's unlocked moves'''
        embed=discord.Embed(title="<a:green_flame:791074893449134080>Stats<a:green_flame:791074893449134080>", color=0xa43232)
       
        embed.set_author(name=f"[Profile]",icon_url=ctx.message.author.avatar_url) 
      
        player1 = await database.load_player(ctx.message.author.id)
        player1.name = ctx.author.name

        text = "\n\n`[Moves unlocked]` "
        for move in player1.moves:
            text += f"\n**[{id_to_move[int(move)]} {id_to_move_emoji[int(move)]}]**"

        embed.add_field(name=f"\n\n`[{ctx.message.author.name} - lvl.{player1.level['lvl']}]`", value=text, inline=False)
        await ctx.message.channel.send(embed=embed)


    @commands.command(aliases=["Inventory", "inv"])
    async def inventory(self, ctx):
        ''': shows the user's inventory'''
        player = await database.load_player(ctx.author.id)
        items = player.inventory
        text = "⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻\n"
        for item in items:
            text += f"**• {item.name}** - `x{item.amount}`  {item.icon}" + "\n"
        text += "⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻"
        embed=discord.Embed(title="<a:purple_flame:791527934057775164>[Inventory]<a:purple_flame:791527934057775164>", color=0xa43232)
        embed.add_field(name="Items: ", value=text)
        await ctx.channel.send(embed=embed)

    @commands.command(aliases=["Info", "information"])
    async def info(self, ctx, *,content: commands.clean_content=None):
        ''': shows the item information'''
        
        item_info = None
        if str(content) in item_list:
            item_info = item_list[str(content)]
        else :
            for key in item_list:
                item = item_list[key]
                if str(content).lower() in item["name"].lower():
                    item_info = item
                    break

        if item_info == None:
            await ctx.channel.send(f"No item **[{content}]** found! use `.info <item id || name>`")
            return
        
        text = "⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻\n"+ item_info["description"] +"\n⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻"
        embed=discord.Embed(title=f"{item_info['icon']}**[{item_info['name']}]**{item_info['icon']}", color=0xa43232)
        embed.add_field(name="Description: ", value=text)
        embed.set_image(url=item_info["thumbnail"])
        await ctx.channel.send(embed=embed)

    @commands.command(aliases=["Upgrade", "up"])
    async def upgrade(self, ctx, *, content: commands.clean_content=None):
        player = await database.load_player(ctx.author.id)

        if content == None:
            await ctx.message.channel.send(f"-upgrade <stat> <# of points> . **Available Points:** {player.misc['Upgrade Points']}  <:plus:795070844745154590>")
            return

        temporary = content.split(" ")

        if len(temporary) != 2:
            await ctx.message.channel.send(f"-upgrade <stat> <# of points> . **Available Points:** {player.misc['Upgrade Points']}  <:plus:795070844745154590>")
            return

        stat_upgraded = None
        points_used = 0

        try:
            points_used = int(temporary[1])
        except:
            await ctx.message.channel.send(f"-upgrade <stat> <# of points> . **Available Points:** {player.misc['Upgrade Points']}  <:plus:795070844745154590>")
            return
        
        if points_used <= 0:
            await ctx.message.channel.send(f"No negatives! -upgrade <stat> <# of points> . **Available Points:** {player.misc['Upgrade Points']}  <:plus:795070844745154590>")
            return  

        for key in player.stats:
            if key.lower() == temporary[0].lower():
                stat_upgraded = key
    
        if points_used > player.misc["Upgrade Points"]:
            await ctx.message.channel.send(f"You do not have enough points to upgrade by **{points_used}**. Missing **{points_used - player.misc['Upgrade Points']}** points.")
            database.save_player(player)
            return
        
        if stat_upgraded == None:
            await ctx.message.channel.send(f"-upgrade <stat> <# of points> . **Available Points:** {player.misc['Upgrade Points']}  <:plus:795070844745154590>")
            database.save_player(player)
            return

        player.stats[stat_upgraded] += points_used
        player.misc["Upgrade Points"] = max(0, player.misc["Upgrade Points"] - points_used)
        player.max_energy = 9 + player.stats["Stamina"]
        await ctx.message.channel.send(f"Upgraded **{stat_upgraded}** {stats_to_emote[stat_upgraded.lower()]} By **{points_used}** points. ")
        database.save_player(player)


def setup(bot):
    bot.add_cog(profile(bot))