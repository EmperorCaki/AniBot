from json import dump, load, loads
import requests


def uwu_encode(plainText):
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


def uwu_decode(encryptedText):
    decryptedText, ordText, binText = '', [], []
    for enchryptedChar in encryptedText.split('umu'):
        binNumber = ''
        if enchryptedChar == '':
            break
        for n in enchryptedChar.split():
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


def link_accounts(discordAccountID, anilistAccount):
    fileName = 'data/linked_accounts.json'
    linkedAccounts = load(open(fileName))
    print(linkedAccounts)
    if discordAccountID in linkedAccounts.keys():
        if linkedAccounts[discordAccountID] == anilistAccount:
            return f'Your account is already linked to {linkedAccounts[discordAccountID]}.'
        else:
            linkedAccounts[discordAccountID] = anilistAccount
            dump(linkedAccounts, open(fileName, 'w'))
            return f'Your account has successfully been updated and is now linked to {linkedAccounts[discordAccountID]}'
    else:
        linkedAccounts[discordAccountID] = anilistAccount
        dump(linkedAccounts, open(fileName, 'w'))
        return f'Your account has successfully been linked to {linkedAccounts[discordAccountID]}'


def make_post_request_to_anilist_API(query, variables):
    # Make the HTTPS Api request
    response = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': variables})
    return loads(response.text), response.status_code
