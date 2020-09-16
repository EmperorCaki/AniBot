import discord
from discord.ext import commands
import re
import uwuify
from random import choice
from random import randint
import functions


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.eightballAnswers = ('As I see it, yes.',
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
                                 'You may rely on it.')

    # COMMANDS ---------------------------------------------------------------------------------------------------------

    @commands.command(name='Ping', aliases=['ping'], help='Pong!')
    async def ping(self, ctx):
        embed = discord.Embed(
            title='Pong!',
            description=f':ping_pong: {int(round(self.client.latency, 3) * 1000)}ms',
            colour=randint(0, 0xffffff)
        )
        await ctx.send(embed=embed)

    @commands.command(name='Encode', aliases=['encode', 'Encrypt', 'encrypt'],
                      help='Encodes a message into "uwu encryption".')
    async def encode(self, ctx, *, message):
        replies = re.findall('.{0,2000}', functions.uwu_encode(message))
        for reply in replies:
            if reply:
                await ctx.send(reply)

    @commands.command(name='Decode', aliases=['decode', 'Decrypt', 'decrypt'],
                      help='Decodes a message from "uwu encryption".')
    async def decode(self, ctx, *, message):
        await ctx.send(functions.uwu_decode(message))

    @commands.command(name='Uwuify', aliases=['uwuify'],
                      help='Uwufies a message.')
    async def uwuify(self, ctx, *, message):
        await ctx.send(uwuify.uwu(message))

    @commands.command(name='8Ball', aliases=['8ball'], help='Ask a question and you shall receive an answer.')
    async def eightball(self, ctx, *, question):
        embed = functions.create_embed_fun('Magic 8Ball', '8Ball')
        for q in question.split('\n'):
            embed.add_field(name=q, value=choice(self.eightballAnswers))
        await ctx.send(embed=embed)

    @commands.command(name='Calculate', aliases=['calculate', 'C', 'c', 'Roll', 'roll', 'R', 'r'],
                      help='Performs math calculations and rolls dice (eg, 1d20, 2d6). '
                           'Separate different equations with a space. '
                           'Allowed operators are:\n + - x * / // ^ % ( )')
    async def calculate(self, ctx, *, calculations: str):
        calculations = calculations.replace('D', 'd')
        if not bool(re.match('^[1234567890dx+-/*^%() ]+$', calculations)):
            print(calculations)
            x = 5 + '5'
        displayCalculations = {}
        calculationsTotal = ''
        calculationTotals = []
        allCalculations = calculations.split(' ')
        for i in range(len(allCalculations)):
            calculationTotal = ''
            # if '+' in allRolls[roll] or '-' in allRolls[roll] or 'd' not in allRolls[roll]:
            displayCalculations[allCalculations[i] + '#' * i] = []
            calculations = allCalculations[i].replace('-', '|-?').replace('+', '|+?').replace('*', '|*?')\
                .replace('//', '|_?').replace('/', '|/?').replace('^', '|**?').replace('x', '|*?')
            calculations = calculations.split('|')
            for j in range(len(calculations)):
                if 'd' in calculations[j]:  # If the calculation contains dice then roll and add the dice to the total.
                    opening = '('
                    closing = ') '
                    if calculations[j][0] == '(' and calculations[j][-1] == ')':
                        pass
                    elif calculations[j][0] == '(':
                        opening = '(('
                        closing = ') '
                    elif calculations[j][-1] == ')':
                        opening = '('
                        closing = ')) '
                    calculations[j] = calculations[j].replace('(', '').replace(')', '')
                    if '?' in calculations[j]:
                        opening = calculations[j].split('?')[0] + ' ('
                        numOfRolls = int(calculations[j].split('d')[0].split('?')[1])
                        diceSize = int(calculations[j].split('d')[1])
                    else:
                        numOfRolls = int(calculations[j].split('d')[0])
                        diceSize = int(calculations[j].split('d')[1])
                    calculationTotal += opening
                    displayCalculations[allCalculations[i] + '#' * i].append(opening.replace('**', '^'))
                    for _ in range(numOfRolls):
                        rollResult = randint(1, diceSize)
                        displayCalculations[allCalculations[i] + '#' * i].append('+ ' + str(rollResult) + ' ')
                        calculationTotal += '+' + str(rollResult)
                    calculationTotal += closing
                    displayCalculations[allCalculations[i] + '#' * i].append(closing)

                else:
                    calculation = calculations[j].replace('_', '//').split('?')
                    if len(calculation) > 1:
                        calculationTotal += calculation[0] + calculation[1]
                        displayCalculations[allCalculations[i] + '#' * i].append(
                            calculation[0].replace('**', '^').replace('*', '\*') + ' ' + calculation[1] + ' ')
                    elif calculation[0] is int:
                        calculationTotal += '+' + calculation[0]
                        displayCalculations[allCalculations[i] + '#' * i].append('+ ' + calculation[0] + ' ')
                    else:
                        calculationTotal += calculation[0]
                        displayCalculations[allCalculations[i] + '#' * i].append(calculation[0].replace('**', '^') + ' ')
            calculationsTotal += '+(' + calculationTotal + ')'
            calculationTotals.append(calculationTotal.strip('+ '))

        embed = functions.create_embed_fun('Calculator & Dice Roller', 'Dice')
        try:
            if len(allCalculations) > 1:
                embed.add_field(name='Total', inline=False,
                                value=f'{round(eval(calculationsTotal), 2)}\n'
                                      f'`{"".join("".join(x) for x in displayCalculations.values()).strip("+").strip(" ")}`'
                                )
            for calculation, calculations, total in zip(displayCalculations.keys(), displayCalculations.values(),
                                                        calculationTotals):
                embed.add_field(name=calculation.replace('#', ''),
                                value=f'{round(eval(total))}\n'
                                      f'`{"".join(calculations).strip("+").strip(" ").replace("(*+* *", "(*")}`')
            await ctx.send(embed=embed)
        except SyntaxError:
            await ctx.send('Make sure you use an equal amount of left and right brackets!')

    # COMMAND ERRORS ---------------------------------------------------------------------------------------------------

    @eightball.error
    async def error_eightball(self, ctx):
        await ctx.send('Make sure you ask a question!')

    @calculate.error
    async def error_calculate(self, ctx, error):
        # if isinstance(error, commands.errors.MissingRequiredArgument)
        await ctx.send('Make sure to only use the allowed operands `+ - / // * ^ % ( )`\n'
                       'And to enter rolls in the format of <NumOfDice>d<DiceType>\n eg `2d6`')
        # embed = functions.create_embed_fun('Calculator & Dice Roller', 'Dice')


def setup(client):
    client.add_cog(Fun(client))
