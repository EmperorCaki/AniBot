import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from uwuify import uwu_text
import re
from uwucipher import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('PREFIX')
bot = commands.Bot(command_prefix=f'{PREFIX} ')


@bot.event
async def on_ready():
    print(f'{bot.user.name}(Bot) has connected to Discord!')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(f'{PREFIX} help'))


@bot.command(name='encode', help='Encodes a message into "uwu encryption".', aliases=['encrypt'])
async def encode(ctx):
    channel = ctx.message.channel
    content = ctx.message.content.replace("uwu encode", "").replace("uwu encrypt", "").strip()
    reply = re.findall('.{2000}', uwu_encode(content))
    for i in reply:
        await channel.send(i)


@bot.command(nam='decode', help='Decodes a message from "uwu encryption".', aliases=['decrypt'])
async def decode(ctx):
    channel = ctx.message.channel
    content = ctx.message.content.replace("uwu decode", "").replace("uwu decrypt", "").strip()
    reply = re.findall('.{2000}', uwu_decode(content))
    for i in reply:
        await channel.send(i)


@bot.command(name='uwuify', help='Uwufies a message.')
async def uwuify(ctx):
    channel = ctx.message.channel
    content = ctx.message.content.replace("uwu uwuify", "").strip()
    await channel.send(uwu_text(content))


print('Connecting...')
bot.run(TOKEN)
