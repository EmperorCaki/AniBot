import discord
from discord.ext import commands
import re
import uwuify
from random import choice
from pprint import pprint
from random import randint
import functions


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    # COMMANDS ---------------------------------------------------------------------------------------------------------

    @commands.command(name='Ping', help='Pong!', aliases=['ping'])
    async def ping(self, ctx):
        embed = discord.Embed(
            title='Pong!',
            description=f':ping_pong: {int(round(self.client.latency, 3) * 1000)}ms',
            colour=randint(0, 0xffffff)
        )
        await ctx.send(embed=embed)

    @commands.command(name='Encode', help='Encodes a message into "uwu encryption".',
                      aliases=['encode', 'Encrypt', 'encrypt'])
    async def encode(self, ctx, *, message):
        replies = re.findall('.{0,2000}', functions.uwu_encode(message))
        for reply in replies:
            if reply:
                await ctx.send(reply)

    @commands.command(name='Decode', help='Decodes a message from "uwu encryption".',
                      aliases=['decode', 'Decrypt', 'decrypt'])
    async def decode(self, ctx, *, message):
        await ctx.send(functions.uwu_decode(message))

    @commands.command(name='Uwuify', help='Uwufies a message.', aliases=['uwuify'])
    async def uwuify(self, ctx, *, message):
        await ctx.send(uwuify.uwu(message))

    @commands.command(name='8Ball', help='Ask a question and you shall receive an answer.', aliases=['8ball'])
    async def eightball(self, ctx, *, question):
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
        embed = discord.Embed(title=question, description=answer, colour=randint(0, 0xffffff))
        embed.set_author(name=ctx.bot.user.name, icon_url=functions.get_image_url('BotPFP'))
        embed.set_thumbnail(url=functions.get_image_url('8Ball'))
        pprint(ctx)
        await ctx.send(embed=embed)

    @commands.command(name='Roll', help='Simulates rolling dice. <NumOfDice>d<DiceType> [eg, 2d6 4d8 1d20]',
                      aliases=['roll'])
    async def roll(self, ctx, *, rolls: str):
        diceRolls = {}
        totalValue = int()
        rolls = rolls.split(' ')
        rolls.sort()
        for roll in range(len(rolls)):
            numOfRolls = int(rolls[roll].lower().split('d')[0])
            diceSize = int(rolls[roll].lower().split('d')[1])
            diceRolls[rolls[roll]+'-'*roll] = []
            for _ in range(numOfRolls):
                rollResult = randint(1, diceSize)
                diceRolls[rolls[roll]+'-'*roll].append(str(rollResult))
                totalValue += rollResult
        embed = discord.Embed(title='Dice Rolls', colour=randint(0, 0xffffff))
        embed.set_thumbnail(url=functions.get_image_url('Dice'))
        embed.add_field(name='Total', value=str(totalValue), inline=False)
        for dice, rolls in diceRolls.items():
            embed.add_field(name=dice.replace('-', ''), value=', '.join(rolls))
        await ctx.channel.send(', '.join(diceRolls), embed=embed)

    # COMMAND ERRORS ---------------------------------------------------------------------------------------------------

    @eightball.error
    async def error_eightball(self, ctx, error):
        await ctx.send('Make sure to ask a question!')

    @roll.error
    async def error_roll(self, ctx, error):
        await ctx.send('Make sure to enter rolls in the format of <NumOfDice>d<DiceType>\n eg `2d6`')
        embed = discord.Embed(title='Dice Rolls', colour=randint(0, 0xffffff))
        embed.set_author(name='Fun Commands')
        embed.set_thumbnail(url=functions.get_image_url('Dice'))


def setup(client):
    client.add_cog(Fun(client))
