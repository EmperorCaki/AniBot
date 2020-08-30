from json import dump, load


def LinkAccounts(discordacc, anilistacc):
    filename = 'txtLinkedAccounts.txt'
    linkedaccounts = load(open(filename))
    if discordacc in linkedaccounts.keys():
        return f'Your account has already been linked to {linkedaccounts(discordacc)}'
    else:
        linkedaccounts[discordacc] = anilistacc
        dump(linkedaccounts, open(filename, 'w'))
        return 'Your account has successfully been linked.'
