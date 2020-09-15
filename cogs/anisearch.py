import discord
from discord.ext import commands
from dpymenus.exceptions import PagesError
import functions


class Anilist(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='Anime', help='Search for an anime.', aliases=['anime'])
    async def anime(self, ctx, *, title):
        media = 'ANIME'
        try:
            menu = functions.search_anime_manga(ctx, media, title)
            if menu:
                await menu.open()
            else:
                await ctx.send('No anime was found or there was an error in the process')

        except TypeError:
            await ctx.send('No anime was found or there was an error in the process')

        except PagesError:
            await ctx.send(embed=menu.page)

    @commands.command(name='Manga', help='Search for a manga.', aliases=['manga'])
    async def manga(self, ctx, *, title):
        media = 'MANGA'
        try:
            menu = functions.search_anime_manga(ctx, media, title)
            if menu:
                await menu.open()
            else:
                await ctx.send('No manga was found or there was an error in the process')

        except TypeError:
            await ctx.send("No manga was found or there was an error in the process")

        except PagesError:
            await ctx.send(embed=menu.page)

    @commands.command(name='Character', help='Search for an anime/manga character.', aliases=['character'])
    async def character(self, ctx, *, character):
        try:
            menu = functions.search_character(ctx, character)
            if menu:
                await menu.open()
            else:
                await ctx.send('No character was found or there was an error in the process')

        except TypeError:
            await ctx.send('No character was found or there was an error in the process')

        except PagesError:
            await ctx.send(embed=menu.page)

    @commands.command(name='User', help='Search for an anilist user.', aliases=['user'])
    async def user(self, ctx, *, user=None):
        if user is None:
            user = functions.get_linked_account(str(ctx.author.id))
            if user is None:
                await ctx.send('Enter a user to search or set a linked account to search by default.')
                return
        try:
            menu = functions.search_user(ctx, user)
            if menu:
                await menu.open()
            else:
                await ctx.send('No user was found or there was an error in the process')

        except TypeError:
            await ctx.send('No user was found or there was an error in the process')

        except PagesError:
            await ctx.send(embed=menu.page)

    @commands.command(name='Linkaccounts', help='Links an anilist username to your discord account, allowing you to use the search for user command without specifying a user.', aliases=['linkaccounts'])
    async def link_accounts(self, ctx, *, user: str):
        functions.link_accounts(str(ctx.author.id), user)



def setup(client):
    client.add_cog(Anilist(client))
