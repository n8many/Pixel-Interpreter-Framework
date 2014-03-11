from commands.command import Command
from alsaaudio import Mixer


class Volume(Command):
    def __init__(self):
        self.keywords = ['volume','turn','sound']

    def isNumber(self, word):
        try:
            int(word)
            return True
        except:
            return False

    def run(self, commandlist):
        mixer = Mixer()

        if len(commandlist) == 1:
            if mixer.getmute():
                mixer.setmute(0)
            else:
                mixer.setmute(1)
        else:
            command = {'mode':'set'}
            for i in xrange(0, len(commandlist)-1):
                pass
