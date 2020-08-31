from json import dump, load, loads
import requests


def uwu_encode(plaintext):
    encryption, ordtext, bintext = '', [], []
    for i in plaintext:
        ordtext.append(ord(i))
    for i in ordtext:
        bintext.append(bin(i))
    for i in bintext:
        for i in i[2:]:
            # print(i)
            if i == '0':
                encryption += 'owo '
            if i == '1':
                encryption += 'uwu '
        encryption += 'umu '
    return (encryption)


def uwu_decode(encryptedtext):
    decrypted, ordtext, bintext = '', [], []
    for i in encryptedtext.split('umu'):
        x = ''
        if i == '':
            break
        for i in i.split():
            if i == 'owo':
                x += '0'
            if i == 'uwu':
                x += '1'
        bintext.append(x)
    for i in bintext:
        ordtext.append(int(f'0b{i}', 0))
    for i in ordtext:
        decrypted += chr(i)
    return (decrypted)

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
