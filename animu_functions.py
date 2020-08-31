from json import dump, load, loads
import requests


def link_accounts(discordAccountID, anilistAccount):
    fileName = 'data_linked_acounts.txt'
    linkedAccounts = load(open(fileName))
    if discordAccountID in linkedAccounts.keys():
        return f'Your account has already been linked to {linkedAccounts(discordAccountID)}'
    else:
        linkedAccounts[discordAccountID] = anilistAccount
        dump(linkedAccounts, open(fileName, 'w'))
        return 'Your account has successfully been linked.'


def make_post_request_to_anilist_API(query, variables):
    # Make the HTTP Api request
    response = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': variables})
    return loads(response.text)
