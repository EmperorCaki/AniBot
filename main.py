import os
from random import choice
import discord
import requests
from discord.ext import commands, tasks
from dotenv import load_dotenv
import json
import functions


def get_prefix(client, message):
    config = json.load(open('data/server_config.json'))
    return config[str(message.guild.id)]['prefix']


load_dotenv()
Token = os.getenv('DISCORD_TOKEN')
DefaultPrefix = os.getenv('PREFIX')
Client = commands.Bot(command_prefix=get_prefix)

for file in os.listdir('./cogs'):
    if file.endswith('.py') and file != '_template.py':
        print(f'Loading {file}')
        Client.load_extension(f'cogs.{file[:-3]}')


@tasks.loop(seconds=120)
async def change_status():
    statuses = json.load(open('data/bot_config.json'))['Statuses']
    await Client.change_presence(activity=discord.Game(choice(statuses)))


@Client.event
async def on_ready():
    print(f'{Client.user.name} has connected to Discord!')
    change_status.start()


@Client.event
async def on_guild_join(guild):
    config = json.load(open('data/server_config.json'))
    config[str(guild.id)] = {}
    config[str(guild.id)]['prefix'] = DefaultPrefix
    json.dump(config, open('data/server_config.json', 'w'), indent=4)


@Client.event
async def on_guild_remove(guild):
    config = json.load(open('data/server_config.json'))
    config.remove(str(guild.id))
    json.dump(config, open('data/server_config.json', 'w'), indent=4)


@Client.command(name='Load', help='Loads a specified extension/s.', aliases=['load'])
async def load_cog(ctx, *, extensions):
    embed = functions.create_embed_main('Load Extension/s')
    if functions.is_bot_admin(ctx.message.author.id):
        for extension in extensions.split():
            message = 'Has been loaded.'
            try:
                Client.load_extension(f'cogs.{extension.lower()}')
            except:
                message = 'Doesn\'t exist or is already loaded.'
            finally:
                embed.add_field(name=extension.title(), value=message, inline=False)
    else:
        embed.description = 'You don\'t have permission to do that!'
    await ctx.send(embed=embed)


@Client.command(name='Unload', help='Unloads a specified extension/s.', aliases=['unload'])
async def unload_cog(ctx, *, extensions):
    embed = functions.create_embed_main('Unload Extension/s')
    if functions.is_bot_admin(ctx.message.author.id):
        for extension in extensions.split():
            message = 'Has been unloaded.'
            try:
                Client.unload_extension(f'cogs.{extension.lower()}')
            except:
                message = 'Doesn\'t exist or isn\'t loaded.'
            finally:
                embed.add_field(name=extension.title(), value=message, inline=False)
    else:
        embed.description = 'You don\'t have permission to do that!'
    await ctx.send(embed=embed)


@Client.command(name='Reload', help='Reloads a specified extension/s.', aliases=['reload'])
async def reload_cog(ctx, *, extensions):
    embed = functions.create_embed_main('Reload Extension/s')
    if functions.is_bot_admin(ctx.message.author.id):
        for extension in extensions.split():
            message = 'Has been reloaded.'
            try:
                Client.reload_extension(f'cogs.{extension.lower()}')
            except:
                message = 'Doesn\'t exist or isn\'t loaded.'
            finally:
                embed.add_field(name=extension.title(), value=message, inline=False)
    else:
        embed.description = 'You don\'t have permission to do that!'
    await ctx.send(embed=embed)


@Client.command(name='Adminify', help='Promotes the specified user/s to an AniAdmin.', aliases=['adminify'])
async def adminify(ctx, *, users):
    embed = functions.create_embed_main('Adminify')
    if functions.is_bot_admin(ctx.message.author.id):
        botConfig = json.load(open('data/bot_config.json'))
        users = users.split(' ')
        for user in users:
            user = Client.get_user(int(user.replace('<@!', '').replace('>', '')))
            if user.id in botConfig['AniAdmins']:
                embed.add_field(name=user.display_name, value=f'They\'re already an AniAdmin!', inline=False)
            elif user.bot:
                if user.id == Client.user.id:
                    embed.add_field(name=user.display_name, value='Is already its own admin!', inline=False)
                else:
                    embed.add_field(name=user.display_name, value='You can\'t make a bot an AniAdmin!', inline=False)
            else:
                botConfig['AniAdmins'].append(user.id)
                embed.add_field(name=user.display_name, value='Is now an AniAdmin!', inline=False)
        json.dump(botConfig, open('data/bot_config.json', 'w'), indent=4)
    else:
        embed.description = 'You don\'t have permission to do that!'
    await ctx.send(embed=embed)


@Client.command(name='Diminify', help='Demotes the specified AniAdmin/s to just a user.', aliases=['diminify'])
async def diminify(ctx, *, users):
    embed = functions.create_embed_main('Diminify')
    if functions.is_bot_admin(ctx.message.author.id):
        botConfig = json.load(open('data/bot_config.json'))
        users = users.split(' ')
        for user in users:
            user = Client.get_user(int(user.replace('<@!', '').replace('>', '')))
            if user.id not in botConfig['AniAdmins']:
                embed.add_field(name=user.display_name, value=f'They\'re already not an AniAdmin!', inline=False)
            else:
                botConfig['AniAdmins'].remove(user.id)
                embed.add_field(name=user.display_name, value='Is no longer AniAdmin!', inline=False)
        json.dump(botConfig, open('data/bot_config.json', 'w'), indent=4)
    else:
        embed.description = 'You don\'t have permission to do that!'
    await ctx.send(embed=embed)


@Client.command(name='Saveimage', help='Adds an image url to the stored urls.', aliases=['saveimage'])
async def save_image_url(ctx, name: str, url: str):
    name = name.title()
    embed = functions.create_embed_main('Save Image')
    try:
        requests.get(url).status_code == 200
    except:
        embed.title = 'Please enter a valid image url!'
        await ctx.send(embed=embed)
        return
    embed.set_image(url=url)
    if functions.is_bot_admin(ctx.message.author.id):
        botConfig = json.load(open('data/bot_config.json'))
        if name not in botConfig['URLs'].keys() and url not in botConfig['URLs'].values():
            botConfig['URLs'][name] = url
            json.dump(botConfig, open('data/bot_config.json', 'w'), indent=4)
            embed.add_field(name=name, value='The specified image has been saved.', inline=False)
        elif url in botConfig['URLs'].values():
            urlName = list(botConfig['URLs'].keys())[list(botConfig['URLs'].values()).index(url)]
            embed.add_field(name=name, value=f'The specified image is already saved as "{urlName}"', inline=False)
        else:
            nameURL = botConfig['URLs'][name]
            embed.add_field(
                name=name,
                value=f'The specified image name already has [this image]({nameURL}) saved under it!',
                inline=False)
    else:
        embed.title = 'You don\'t have permission to do that!'
    await ctx.send(embed=embed)


# @save_image_url.error
# async def error_save_image_url(ctx, error):
#     if isinstance(error, commands.errors.)

print('\nConnecting...')
Client.run(Token)
