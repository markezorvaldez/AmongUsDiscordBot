import json
import discord
from discord.ext import commands

with open('config.json', 'r') as f:
    config = json.load(f)

bot = commands.Bot(command_prefix=config['prefix'])
    
@bot.command()
async def print(ctx, *, arg):
    await ctx.send(arg)

bot.run(config['token'])