import discord
from discord.ext import commands
import json

Client = discord.Client


class Config(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='Prefix', help='Set AniBot\'s prefix for the server.', aliases=['prefix'])
    async def change_prefix(self, ctx, prefix):
        config = json.load(open('data/server_config.json'))
        config[str(ctx.guild.id)]['prefix'] = prefix
        json.dump(config, open('data/server_config.json', 'w'), indent=4)
        embed = discord.Embed(colour=0x000000)
        embed.set_author(
            name=ctx.guild.name,
            url=f'https://discord.com/channels/{ctx.channel.id}',
            icon_url=ctx.guild.icon_url
        )
        embed.add_field(name='Prefix is now:', value=prefix)
        await ctx.send(embed=embed)

    @commands.command(name='Servers', help='Returns all servers the bot is in.', aliases=['servers'])
    async def servers(self, ctx):
        print('Logged in as')
        print(ctx.bot.user.name)
        print(ctx.bot.user.id)
        print('------')

        print('Servers connected to:')
        for guild in ctx.bot.guilds:
            print(guild.name)
            print(guild.id)
            await ctx.send(f'{guild.name}: {guild.id}')


def setup(client):
    client.add_cog(Config(client))
