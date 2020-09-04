from json import dump, load, loads
from pprint import pprint
import requests


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
    linkedAccounts = load(open('data/linked_accounts.json'))
    print(linkedAccounts)
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


def make_post_request_to_anilist_API(query: str, variables: dict):
    # Make the HTTPS Api request
    response = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': variables})
    return loads(response.text), response.status_code


def is_bot_admin(userID: int):
    if userID in load(open('data/bot_config.json'))['AniAdmins']:
        return True
    else:
        return False


def get_image_url(image: str):
    return load(open('data/bot_config.json'))['URLs'][image]


# Here we define our query as a multi-line string
Query = """
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

# Define our query variables and values that will be used in the query request
Variables = {
    'id': 20665
}

# response, status = make_post_request_to_anilist_API(query, variables)
# print(status)
# pprint(response["data"])
