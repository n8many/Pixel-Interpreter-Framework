from commands import *
import config


class Interp(object):
    def __init__(self, cmd):
        logins = config.logins
        # FIXME: The c.__module... duplication is bad, find a way to
        # clean it up.
        self.commands = [
                c(logins[c.__module__.split('.')[-1]]) if c.needsPassword() else c()
                    for c in command.Command.__subclasses__()
        ]

        self.interpret(cmd)

    def interpret(self, cmdstring):
        words = cmdstring.split()
        commands = list()
        for w in words:
            for key in ['and', 'And', 'also', 'Also']:
                if w == key:
                    commands.append (words[0:words.index(key)])
                    words = words[words.index(key)+1:]
                    break
        commands.append(words)

        lastcmd = False
        for order in commands:
            contains = False
            for word in order:
                if contains == True:
                    break
                for command in self.commands:
                    if command.hasKeyword(word):
                        contains = True
                        lastcmd = command
                        command.run(order)
                        break
            if not contains:
                if lastcmd:
                    lastcmd.run(order)
