import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

from animu_functions import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('PREFIX')

bot = commands.Bot(command_prefix='ani ')


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)

    print(
        f'{bot.user} is connected to the following server:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Server Members:\n - {members}\n')

    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Anime Binging"))


@bot.event
async def on_command_error(ctx, error):
    channel = ctx.message.channel
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')
    elif isinstance(error, commands.errors.BadArgument):
        await ctx.send('That didn\'t work. Make sure you enter the correct information into your command!')
    else:
        await channel.send('Sorry but that command didn\'t work. Try again!')


@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    channel = ctx.message.channel
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await channel.send(response)


@bot.command(name='roll_dice', help='Simulates rolling dice. [Enter two numbers]')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    channel = ctx.message.channel
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await channel.send(', '.join(dice))


@bot.command(name='mywebsites', help='Provides links to my websites.')
async def mywebsites(ctx):
    channel = ctx.message.channel
    embed = discord.Embed(
        title='Title',
        description='This is a desc.',
        colour=discord.Colour.blue(),
    )
    embed.set_author(name='Ani Bot',
                     icon_url='https://cdn.discordapp.com/attachments/689431256789942291/690792116183367720/Lelouch.jpg',
                     url='https://hakea.redbubble.com')
    embed.set_image(url='https://cdn.discordapp.com/attachments/689431256789942291/690792116183367720/Lelouch.jpg')

    await channel.send(embed=embed)


@bot.command(name='testembed', help='embed testing')
async def testembed(ctx):
    channel = ctx.message.channel
    embed = discord.Embed(
        title='Title',
        description='This is a desc.',
        colour=discord.Colour.blue(),
    )
    embed.set_author(name='Ani Bot',
                     icon_url='https://cdn.discordapp.com/attachments/689431256789942291/690792116183367720/Lelouch.jpg',
                     url='https://hakea.redbubble.com')
    embed.set_image(url='https://cdn.discordapp.com/attachments/689431256789942291/690792116183367720/Lelouch.jpg')

    await channel.send(embed=embed)


# @bot.command(name='Link Anilist Account', help='Links your discord account to your anilist account.')
# async def link(ctx, anilist_account):
#     linkaccounts(ctx.author.id, anilist_account)


bot.run(TOKEN)
