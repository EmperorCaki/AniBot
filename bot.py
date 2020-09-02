import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from json import dump, load


def get_prefix(message):
    config = load(open('data/config.json'))
    return config[str(message.guild.id)]['prefix']


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('PREFIX')
client = commands.Bot(command_prefix=get_prefix)

for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        print(f'Loading {file}')
        client.load_extension(f'cogs.{file[:-3]}')


@client.event
async def on_ready():
    print(f'{client.user.name} ({os.path.basename(__file__)}) has connected to Discord!')
    await client.change_presence(status=discord.Status.online, activity=discord.Game(f'{PREFIX} help'))


@client.event
async def on_guild_join(guild):
    settings = load(open('data/config.json'))
    print(settings)
    if settings[str(guild.id)]:
        settings[str(guild.id)]['prefix'] = PREFIX
        dump(settings, open('data/config.json', 'w'), indent=4)


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} loaded.')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} unloaded.')


print('\nConnecting...')
client.run(TOKEN)
