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
    for binValue in encryptedText.split('umu'):
        binNumber = ''
        if binValue == '':
            break
        for binNumber in binNumber.split():
            if binNumber == 'owo':
                binNumber += '0'
            if binNumber == 'uwu':
                binNumber += '1'
        binText.append(binNumber)
    for binNumber in binText:
        ordText.append(int(f'0b{binNumber}', 0))
    for ordNumber in ordText:
        decryptedText += chr(ordNumber)
    return decryptedText


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
    # Make the HTTPS Api request
    response = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': variables})
    return loads(response.text), response.status_code
