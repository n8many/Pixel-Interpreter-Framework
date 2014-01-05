from commands import *

def interpret(cmdstring):

    words = cmdstring.split()
    commands = list()
    for w in words:
        for key in ['and', 'And', 'also', 'Also']:
            if w == key:
                commands.append (words[0:words.index(key)])
                words = words[words.index(key)+1:]
                break
    commands.append(words)

    for order in commands:
        if command.isKeyword(order[0]):
            command.execute(order[1:])

