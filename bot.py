import json
import logging
import discord
from discord.ext import commands

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

with open('config.json', 'r') as f:
    config = json.load(f)

bot = commands.Bot(command_prefix=config['prefix'])
    
@bot.command(help='Prints any specified text')
async def print(ctx, *, arg):
    await ctx.send(arg)

bot.code = None

@bot.command(help='Gets or sets the Among Us game code')
async def code(ctx, arg=None):
    if not arg:
        await ctx.send(bot.code or "There is no code yet!")
    else:
        bot.code = arg
        await ctx.send("The code is set to %s" % bot.code)
        
bot.run(config['token'])