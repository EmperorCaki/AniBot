import datetime
import json
from pprint import pprint

import aiohttp
import discord

SEARCH_ANIME_MANGA_QUERY = """
query ($id: Int, $page: Int, $search: String, $type: MediaType) {
    Page (page: $page, perPage: 10) {
        media (id: $id, search: $search, type: $type) {
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
            meanScore
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


async def _request(query, variables=None):
    if variables is None:
        variables = {}

    request_json = {"query": query, "variables": variables}

    headers = {"content-type": "application/json"}

    async with aiohttp.ClientSession() as session:
        async with session.post('https://graphql.anilist.co', data=json.dumps(request_json), headers=headers) as response:
            return await response.json()


async def test():
    variables = {"search": 'Sword Art Online', "page": 1, "type": 'ANIME'}
    data = await _request(SEARCH_ANIME_MANGA_QUERY, variables)
    pprint(data)
    return


await test()


async def _search_anime_manga(self, ctx, cmd, entered_title):
    # Outputs MediaStatuses to strings
    MediaStatusToString = {
        # Has completed and is no longer being released
        "FINISHED": "Finished",
        # Currently releasing
        "RELEASING": "Releasing",
        # To be released at a later date
        "NOT_YET_RELEASED": "Not yet released",
        # Ended before the work could be finished
        "CANCELLED": "Cancelled",
    }

    variables = {"search": entered_title, "page": 1, "type": cmd}

    data = (await self._request(SEARCH_ANIME_MANGA_QUERY, variables))["data"]["Page"]["media"]
    print(data)

    if data is not None and len(data) > 0:

        # a list of embeds
        embeds = []

        for anime_manga in data:
            # Sets up various variables for Embed
            link = f"https://anilist.co/{cmd.lower()}/{anime_manga['id']}"
            description = anime_manga["description"]
            title = anime_manga["title"]["english"] or anime_manga["title"]["romaji"]
            if anime_manga.get("nextAiringEpisode"):
                seconds = anime_manga["nextAiringEpisode"]["timeUntilAiring"]
                time_left = str(datetime.timedelta(seconds=seconds))
            else:
                time_left = "Never"

            external_links = ""
            for i in range(0, len(anime_manga["externalLinks"])):
                ext_link = anime_manga["externalLinks"][i]
                external_links += f"[{ext_link['site']}]({ext_link['url']}), "
                if i + 1 == len(anime_manga["externalLinks"]):
                    external_links = external_links[:-2]

            embed = discord.Embed(title=title)
            embed.url = link
            embed.colour = 3447003
            embed.description = self._description_parser(description)
            embed.set_thumbnail(url=anime_manga["coverImage"]["medium"])
            embed.add_field(name="Score", value=anime_manga.get("averageScore", "N/A"))
            if cmd == "ANIME":
                embed.add_field(name="Episodes", value=anime_manga.get("episodes", "N/A"))
                embed.set_footer(text="Status : " + MediaStatusToString[
                    anime_manga["status"]] + ", Next episode : " + time_left + ", Powered by Anilist")
            else:
                embed.add_field(name="Chapters", value=anime_manga.get("chapters", "N/A"))
                embed.set_footer(text="Status : " + MediaStatusToString.get(anime_manga.get("status"),
                                                                            "N/A") + ", Powered by Anilist")
            if external_links:
                embed.add_field(name="Streaming and/or Info sites", value=external_links)
            if anime_manga["bannerImage"]:
                embed.set_image(url=anime_manga["bannerImage"])
            embed.add_field(name="You can find out more",
                            value=f"[Anilist]({link}), [MAL](https://myanimelist.net/{cmd.lower()}/{anime_manga['idMal']}), Kitsu (Soon™)")
            embeds.append(embed)

        return embeds, data

    else:
        return None
