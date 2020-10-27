import asyncio
import discord
import json
import logging
from discord.ext import commands

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

with open('config.json', 'r') as f:
    config = json.load(f)

bot = commands.Bot(command_prefix=config['prefix'])

bot.codes = {}

@bot.command(help='Gets or sets the Among Us game code on the author\'s channel')
async def code(ctx, arg=None):
    if not arg:
        if ctx.author.voice.channel.id in bot.codes:
            await ctx.send('The Among Us code for this channel ({0}) is {1}'.format(ctx.author.voice.channel, bot.codes[ctx.author.voice.channel.id]))
        else:
            await ctx.send('There is no code for this channel ({}) yet!'.format(ctx.author.voice.channel))
    else:
        bot.codes[ctx.author.voice.channel.id] = arg
        await ctx.send('The Among Us code for this channel ({0}) is set to {1}'.format(ctx.author.voice.channel, arg))

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
    await ctx.send('Everyone in {} is now muted'.format(ctx.author.voice.channel))

@bot.command(help='Unmutes everyone in the voice channel')
async def unmuteall(ctx):
    await toggle_mute([await ctx.guild.fetch_member(id) for id in ctx.author.voice.channel.voice_states.keys()], "false")
    await ctx.send('Everyone in {} is now unmuted'.format(ctx.author.voice.channel))

async def toggle_mute(members, toggle):
    await asyncio.gather(*[member.edit(mute=toggle,deafen=toggle) for member in members])

bot.run(config['token'])