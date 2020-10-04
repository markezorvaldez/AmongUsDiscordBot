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

bot.code = None

@bot.command(help='Gets or sets the Among Us game code')
async def code(ctx, arg=None):
    if not arg:
        await ctx.send(bot.code or "There is no code yet!")
    else:
        bot.code = arg
        await ctx.send("The code is set to %s" % bot.code)

@bot.command(help='Mutes specified users')
async def dead(ctx, members: commands.Greedy[discord.Member]):
    await toggle_mute(members, "true")
    await ctx.send('{} you are dead! Be quiet'.format(", ".join(x.mention for x in members)))

@bot.command(help='Unmutes specified users')
async def alive(ctx, members: commands.Greedy[discord.Member]):
    await toggle_mute(members, "false")
    await ctx.send('{} you are alive!'.format(", ".join(x.mention for x in members)))

@bot.command(help='Mutes everyone in the voice channel')
async def muteall(ctx):
    await toggle_mute([await ctx.guild.fetch_member(id) for id in ctx.author.voice.channel.voice_states.keys()], "true")
        
@bot.command(help='Unmutes everyone in the voice channel')
async def unmuteall(ctx):
    await toggle_mute([await ctx.guild.fetch_member(id) for id in ctx.author.voice.channel.voice_states.keys()], "false")

async def toggle_mute(members, toggle):
    for member in members:
        await member.edit(mute=toggle,deafen=toggle)

bot.run(config['token'])