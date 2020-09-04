import discord
from discord.ext import commands
from json import dump, load

Client = discord.Client


class Template(commands.Cog):
    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(Template(client))
