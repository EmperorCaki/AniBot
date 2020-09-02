import discord
from discord.ext import commands
from json import dump, load


class Config(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def change_prefix(self, ctx, prefix):
        settings = load(open('config.json'))
        settings[str(ctx.guild.id)]['prefix'] = prefix
        dump(settings, open('config.json', 'w'), indent=4)
        await ctx.send(f'The prefix in {ctx.guild} has been set to `{prefix}`.')


def setup(client):
    client.add_cog(Config(client))