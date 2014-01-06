import glob

class Interp(object):
    def __init__(self):
        self.cmdmodules = dict()
        self.findCommands()

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

        lastcmd = ''
        for order in commands:
            contains = False
            for command in self.cmdmodules:
                module = self.cmdmodules[command]  
                cmd = module.__dict__[module.name]()
                if cmd.hasKeyword(order[0]):
                    contains = True
                    lastcmd = cmd
                    cmd.run(order[1:])
                    break
            if not contains:
                if lastcmd != '':
                    lastcmd.run(order)
