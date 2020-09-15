import datetime
import re
from json import dump, load, loads
from random import randint
import dpymenus
import requests

_QueryAniManga = """query ($id: Int, $page: Int, $search: String, $type: MediaType) {
  Page(page: $page, perPage: 10) {
    media(id: $id, search: $search, type: $type) {
      id
      idMal
      description(asHtml: false)
      title {
        english
        romaji
      }
      coverImage {
        medium
      }
      bannerImage
      averageScore
      popularity
      genres
      tags {
        name
      }
      season
      seasonYear
      studios {
        nodes {
          name
          siteUrl
        }
      }
      endDate {
        year
        month
        day
      }
      startDate {
        year
        month
        day
      }
      status
      episodes
      chapters
      externalLinks {
        url
        site
      }
      nextAiringEpisode {
        timeUntilAiring
      }
    }
  }
}
"""

_QueryCharacter = """
query ($id: Int, $page: Int, $search: String) {
  Page(page: $page, perPage: 10) {
    characters(id: $id, search: $search) {
      id
      description (asHtml: true),
      name {
        first
        last
        native
      }
      image {
        large
      }
      media {
        nodes {
          id
          type
          title {
            romaji
            english
            native
            userPreferred
          }
        }
      }
    }
  }
}
"""

_QueryUser = """query ($id: Int, $page: Int, $search: String) {
  Page(page: $page, perPage: 10) {
    users(id: $id, search: $search) {
      id
      name
      siteUrl
      avatar {
        large
      }
      bannerImage
      about(asHtml: true)
      statistics {
        anime {
          minutesWatched
          episodesWatched
          meanScore
        }
        manga {
          chaptersRead
          volumesRead
          meanScore
        }
      }
      favourites {
        manga {
          nodes {
            id
            title {
              romaji
              english
              native
              userPreferred
            }
          }
        }
        characters {
          nodes {
            id
            name {
              first
              last
              native
            }
          }
        }
        anime {
          nodes {
            id
            title {
              romaji
              english
              native
              userPreferred
            }
          }
        }
      }
    }
  }
}
"""


def uwu_encode(plainText: str):
    encryptedText, ordText, binText = '', [], []
    for char in plainText:
        ordText.append(ord(char))
    for char in ordText:
        binText.append(bin(char)[2:])
    for char in binText:
        for n in char:
            if n == '0':
                encryptedText += 'owo '
            if n == '1':
                encryptedText += 'uwu '
        encryptedText += 'umu '
    return encryptedText.strip()


def uwu_decode(encryptedText: str):
    decryptedText, ordText, binText = '', [], []
    for encryptedChar in encryptedText.split('umu'):
        binNumber = ''
        if encryptedChar == '':
            break
        for n in encryptedChar.split():
            if n == 'owo':
                binNumber += '0'
            if n == 'uwu':
                binNumber += '1'
        binText.append(f'0b{binNumber}')
    for binNumber in binText:
        ordText.append(int(binNumber, 0))
    for ordNumber in ordText:
        decryptedText += chr(ordNumber)
    return decryptedText


def link_accounts(discordAccountID: str, anilistAccount: str):
    fileName = 'data/linked_accounts.json'
    linkedAccounts = load(open(fileName))
    if discordAccountID in linkedAccounts.keys():
        if linkedAccounts[discordAccountID] == anilistAccount:
            return f'Your account is already linked to {linkedAccounts[discordAccountID]}.'
        else:
            linkedAccounts[discordAccountID] = anilistAccount
            dump(linkedAccounts, open(fileName, 'w'), indent=4)
            return f'Your account has successfully been updated and is now linked to {linkedAccounts[discordAccountID]}'
    else:
        linkedAccounts[discordAccountID] = anilistAccount
        dump(linkedAccounts, open(fileName, 'w'), indent=4)
        return f'Your account has successfully been linked to {linkedAccounts[discordAccountID]}'


def get_linked_account(discordAccountID: str):
    fileName = 'data/linked_accounts.json'
    linkedAccounts = load(open(fileName))
    return linkedAccounts.get(discordAccountID, None)



def is_bot_admin(userID: int):
    if userID in load(open('data/bot_config.json'))['AniAdmins']:
        return True
    else:
        return False


def get_image_url(image: str):
    return load(open('data/bot_config.json'))['URLs'][image]


# Embed Creating -------------------------------------------------------------------------------------------------------


# Anilist Searching ----------------------------------------------------------------------------------------------------


def _create_page(title):
    page = dpymenus.Page(title=title)
    page.set_author(name='Anisearch', icon_url=get_image_url('BotPFP'))
    return page


def _make_post_request_to_anilist_API(query: str, variables: dict):
    # Make the HTTPS Api request
    response = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': variables})
    return loads(response.text), response.status_code


def _format_name(first_name, last_name):  # Combines first_name and last_name and/or shows either of the two
    if first_name and last_name:
        return first_name + ' ' + last_name
    elif first_name:
        return first_name
    elif last_name:
        return last_name
    else:
        return 'No name'


def _clean_html(description):  # Removes html tags
    if not description:
        return ''
    clean = re.compile('<.*?>')
    cleanText = re.sub(clean, '', description)
    return cleanText


def _clean_spoilers(description):  # Removes spoilers using the html tag given by AniList
    if not description:
        return ''
    clean = re.compile('/<span[^>]*>.*</span>/g')
    cleanText = re.sub(clean, '', description)
    return cleanText


def _description_parser(description):  # Limits text to 400characters and 5 lines and adds '...' at the end
    description = _clean_spoilers(description)
    description = _clean_html(description)
    description = '\n'.join(description.split('\n')[:5])
    if len(description) > 400:
        return description[:400] + '...'
    else:
        return description


def _list_maximum(items):  # Limits to 5 strings than adds '+X more'
    if len(items) > 5:
        return items[:5] + ['+ ' + str(len(items) - 5) + ' more']
    else:
        return items


def search_anime_manga(ctx, media, title):
    variables = {'search': title, 'page': 1, 'type': media}

    aniMangas, status = _make_post_request_to_anilist_API(_QueryAniManga, variables)
    aniMangas = aniMangas['data']['Page']['media']

    if status == 200:

        # a list of embeds
        pages = []
        totalNumberOfResults = len(aniMangas)
        resultNumber = 1

        for aniManga in aniMangas:
            # Sets up various variables for Embed
            link = f'https://anilist.co/{media.lower()}/{aniManga["id"]}'
            description = aniManga['description']
            title = f'**{aniManga["title"]["english"]}**\n' if aniManga['title']['english'] is not None else ''
            title += f'*{aniManga["title"]["romaji"]}*'
            # title = f'**{aniManga["title"]["english"]}**\n*{aniManga["title"]["romaji"]}*'
            season = f'{aniManga["season"].title()} {aniManga["seasonYear"]}' if aniManga['season'] else 'N/A'
            if aniManga.get('nextAiringEpisode'):
                seconds = aniManga['nextAiringEpisode']['timeUntilAiring']
                time_left = str(datetime.timedelta(seconds=seconds))
            else:
                time_left = 'Never'

            external_links = ''
            for i in range(0, len(aniManga['externalLinks'])):
                ext_link = aniManga['externalLinks'][i]
                external_links += f'[{ext_link["site"]}]({ext_link["url"]}), '
                if i + 1 == len(aniManga['externalLinks']):
                    external_links = external_links.strip(', ')

            page = _create_page(title)
            page.url = link
            page.colour = randint(0, 0xffffff)
            page.set_thumbnail(url=aniManga['coverImage']['medium'])
            if aniManga['bannerImage']:
                page.set_image(url=aniManga['bannerImage'])

            page.description = _description_parser(description)
            page.add_field(name='Popularity', value=aniManga.get('popularity', 'N/A'))
            page.add_field(name='Score', value=aniManga.get('averageScore', 'N/A'))
            if media == 'ANIME':
                page.add_field(name='Episodes', value=aniManga.get('episodes', 'N/A'))
                page.add_field(name='Season', value=season)
                page.add_field(name='Status', value=aniManga['status'].title().replace('_', ' '))
                page.add_field(name='Next Episode', value=time_left)
            else:
                page.add_field(name='Chapters', value=aniManga.get('chapters', 'N/A'))
                # page.add_field(name='Volumes', value=aniManga.get('volumes', 'N/A'))
                page.add_field(name='Status', value=aniManga['status'].title().replace('_', ' '))

            if aniManga.get('startDate')['year']:
                page.add_field(name='Start Date', value=datetime.date(day=aniManga['startDate']['day'],
                                                                      month=aniManga['startDate']['month'],
                                                                      year=aniManga['startDate']['year']
                                                                      ).strftime('%A %d %B %Y'))
            if aniManga.get('endDate')['year']:
                page.add_field(name='End Date', value=datetime.date(day=aniManga['endDate']['day'],
                                                                    month=aniManga['endDate']['month'],
                                                                    year=aniManga['endDate']['year']
                                                                    ).strftime('%A %d %B %Y'))

            if len(aniManga['genres']) > 0:
                page.add_field(name='Genres', inline=False,
                               value=', '.join(
                                   f'[{genre}](https://anilist.co/search/anime?genres={genre.replace(" ", "%20")})'
                                   for genre in aniManga['genres']))
            if media == 'ANIME':
                page.add_field(
                    name='Studios', inline=False,
                    value=(', '.join(
                        f'[{studio["name"]}]({studio["siteUrl"]})' for studio in aniManga['studios']['nodes']) if
                           aniManga['studios']['nodes'] else 'N/A'))
            page.add_field(
                name='Find out more', inline=False,
                value=f'[Anilist]({link}), [MAL](https://myanimelist.net/{media.lower()}/{aniManga["idMal"]})'
            )
            if external_links:
                page.add_field(name='Stream/Find out more', value=external_links, inline=True)

            page.set_footer(text=f'{media.title()} {resultNumber}/{totalNumberOfResults}')
            resultNumber += 1

            pages.append(page)

        menu = dpymenus.PaginatedMenu(ctx)
        menu.add_pages(pages)
        menu.set_timeout(60)
        menu.persist_on_close()
        menu.show_command_message()
        menu.show_page_numbers()
        menu.show_skip_buttons()
        menu.hide_cancel_button()
        menu.allow_multisession()

        return menu

    else:
        return None


def search_character(ctx, character):
    variables = {'search': character, 'page': 1}

    characters, status = _make_post_request_to_anilist_API(_QueryCharacter, variables)
    characters = characters['data']['Page']['characters']

    if status == 200:

        # a list of embeds
        pages = []
        totalNumberOfResults = len(characters)
        resultNumber = 1

        for character in characters:
            # Sets up various variables for Embed
            link = f'https://anilist.co/character/{character["id"]}'
            character_anime = [f'[{anime["title"]["userPreferred"]}]({"https://anilist.co/anime/" + str(anime["id"])})'
                               for anime in character["media"]["nodes"] if anime["type"] == "ANIME"]
            character_manga = [f'[{manga["title"]["userPreferred"]}]({"https://anilist.co/manga/" + str(manga["id"])})'
                               for manga in character["media"]["nodes"] if manga["type"] == "MANGA"]
            page = _create_page(_format_name(character['name']['first'], character['name']['last']))
            page.url = link
            page.colour = randint(0, 0xffffff)
            page.description = _description_parser(character['description'])
            page.set_thumbnail(url=character['image']['large'])
            if len(character_anime) > 0:
                page.add_field(name='Anime', value='\n'.join(_list_maximum(character_anime)))
            if len(character_manga) > 0:
                page.add_field(name='Manga', value='\n'.join(_list_maximum(character_manga)))
            page.set_footer(text=f'Character {resultNumber}/{totalNumberOfResults}')
            resultNumber += 1
            pages.append(page)

        menu = dpymenus.PaginatedMenu(ctx)
        menu.add_pages(pages)
        menu.set_timeout(60)
        menu.persist_on_close()
        menu.show_command_message()
        menu.show_page_numbers()
        menu.show_skip_buttons()
        menu.hide_cancel_button()
        menu.allow_multisession()

        return menu

    else:
        return None


def search_user(ctx, user):
    variables = {'search': user, 'page': 1}

    users, status = _make_post_request_to_anilist_API(_QueryUser, variables)
    users = users['data']['Page']['users']

    if status == 200:

        # a list of embeds
        pages = []
        totalNumberOfResults = len(users)
        resultNumber = 1

        for user in users:
            # Sets up various variables for Embed
            link = f'https://anilist.co/user/{user["id"]}'
            title = f'[{user["name"]}]({link})'
            title = user['name']

            page = _create_page(title)
            page.url = link
            page.colour = randint(0, 0xffffff)
            page.description = _description_parser(user['about'])

            page.set_thumbnail(url=user['avatar']['large'])
            # if user['bannerImage']:
            #     page.set_image(url=user['bannerImage'])

            page.add_field(name='Mean Score', inline=True,
                           value=f'Anime: {str(round(user["statistics"]["anime"].get("meanScore", "N/A"), 1))}\n'
                                 f'Manga: {str(round(user["statistics"]["manga"].get("meanScore", "N/A"), 1))}'
                           )
            page.add_field(name='Anime Watched', inline=True,
                           value=f'{str(round(user["statistics"]["anime"].get("minutesWatched", 0) / 1440, 2))} Days.\n'
                                 f'{str(user["statistics"]["anime"].get("episodesWatched", 0))} Episodes.'
                           )
            page.add_field(name='Manga Read', inline=True,
                           value=f'{str(user["statistics"]["manga"].get("volumesRead", 0))} Volumes.\n'
                                 f'{str(user["statistics"]["manga"].get("chaptersRead", 0))} Chapters.'
                           )

            for category in 'anime', 'manga', 'characters':
                fav = []
                for node in user['favourites'][category]['nodes']:
                    url_path = category.strip('s')
                    if category == 'characters':
                        name = node['name']
                        title = _format_name(name['first'], name['last'])
                    else:
                        title = node['title']['userPreferred']

                    fav.append(f'[{title}](https://anilist.co/{url_path}/{node["id"]})')

                if fav:
                    page.add_field(name=f'Favorite {category}', value='\n'.join(_list_maximum(fav)))
            page.set_footer(text=f'User {resultNumber}/{totalNumberOfResults}')
            resultNumber += 1
            pages.append(page)

        menu = dpymenus.PaginatedMenu(ctx)
        menu.add_pages(pages)
        menu.set_timeout(60)
        menu.persist_on_close()
        menu.show_command_message()
        menu.show_page_numbers()
        menu.show_skip_buttons()
        menu.hide_cancel_button()
        menu.allow_multisession()

        return menu

    else:
        return None
