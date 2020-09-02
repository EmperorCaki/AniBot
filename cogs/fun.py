import discord
from discord.ext import commands
import re
from uwuify import uwu_text
from functions import *
from random import choice
from pprint import pprint
import matplotlib


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='encode', help='Encodes a message into "uwu encryption".', aliases=['encrypt'])
    async def encode(self, ctx, *, message):
        replies = re.findall('.{0,2000}', uwu_encode(message))
        for reply in replies:
            if reply:
                await ctx.send(reply)

    @commands.command(nam='Decode', help='Decodes a message from "uwu encryption".', aliases=['decrypt'])
    async def decode(self, ctx, *, message):
        await ctx.send(uwu_decode(message))

    @commands.command(name='uwuify', help='Uwufies a message.')
    async def uwuify(self, ctx, *, message):
        await ctx.send(uwu_text(message))

    @commands.command(name='8Ball', help='Ask a question and you shall receive an answer.', aliases=[
        '8ball', 'eightball', 'Eightball', 'EightBall'
    ])
    async def _8ball(self, ctx, *, question):
        answer = choice(['As I see it, yes.',
                         'Ask again later.',
                         'Better not tell you now.',
                         'Cannot predict now.',
                         'Concentrate and ask again.',
                         'Don’t count on it.',
                         'It is certain.',
                         'It is decidedly so.',
                         'Most likely.',
                         'My reply is no.',
                         'My sources say no.',
                         'Outlook not so good.',
                         'Outlook good.',
                         'Reply hazy, try again.',
                         'Signs point to yes.',
                         'Very doubtful.',
                         'Without a doubt.',
                         'Yes.',
                         'Yes – definitely.',
                         'You may rely on it.'])
        embed = discord.Embed(title=question, description=answer)
        embed.set_author(name='ctx',
                         icon_url='https://media.discordapp.net/attachments/695297871976726559/750540404025196624'
                                  '/Lelouch.jpg?width=702&height=702')
        embed.set_thumbnail(url='https://www.jing.fm/clipimg/full/262-2622010_8ball-pool-ball-clip-art.png')
        pprint(ctx)
        await ctx.send(embed=embed)

    @commands.command(name='Ping', help='Pong!', aliases=['ping'])
    async def ping(self, ctx):
        embed = discord.Embed(
            title='Pong!',
            description=f':ping_pong: {int(round(self.client.latency, 3)*1000)}ms',
            colour=choice(list(matplotlib.colors.cnames.values()))
        )
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Fun(client))
