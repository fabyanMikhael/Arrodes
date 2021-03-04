import os, discord, asyncio

from discord.ext import commands

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="-", intents=intents)


TOKEN = os.environ["DISCORD_TOKEN"]

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")
    for cog in os.listdir("./cogs"):
        if cog.endswith(".py"):
            try:
                cog = f"cogs.{cog.replace('.py', '')}"
                bot.load_extension(cog)
                print(f"{cog} Loaded!")
            except Exception as e:
                print(f"{cog} cannot be loaded:")
                raise e


@bot.event
async def on_member_join(member):
    print(f"{member} has joined")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message=message)


bot.run(TOKEN)

