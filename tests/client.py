import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user.name} ({os.path.basename(__file__)}) has connected to Discord!')
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Anime Binging"))


@client.event
async def on_message(ctx):
    if ctx.author == client.user:
        return

    if ctx.content.startswith('hello'):
        await ctx.channel.send('Hello!')


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

print('Connecting...')
client.run(TOKEN)
