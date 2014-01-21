import glob
import config

class Interp(object):
    def __init__(self):
        self.cmdmodules = dict()
        passdict = config.logins
        self.findCommands()
        self.cmd = list()
        for command in self.cmdmodules:
            module = self.cmdmodules[command]
            self.cmd += [module.__dict__[module.name](passdict[module.name]['u'], passdict[module.name]['pass'])]

    def importCommand(self, commandName):
        command = __import__(commandName)
        for c in commandName.split(".")[1:]:
            command = getattr(command, c)
        return command

    def findCommands(self):
        cmdfiles = glob.glob("commands/*py")
        for module in cmdfiles:
            module = module.split("/")[-1].split(".")[0]
            self.cmdmodules[module] = self.importCommand("commands." +
                   module)
        self.cmdmodules.__delitem__('command')
        self.cmdmodules.__delitem__('__init__')

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
            for command in self.cmd:
                if command.hasKeyword(order[0]):
                    contains = True
                    lastcmd = command
                    command.run(order[1:])
                    break
            if not contains:
                if lastcmd:
                    lastcmd.run(order)
