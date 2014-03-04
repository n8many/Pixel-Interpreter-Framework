from commands.command import Command
import beautifulhue

name = 'Lights'

class Lights(Command):
    def __init__(self):
        self.keywords = ['light','lights']

    def run(self, commandlist):
        if len(commandlist) == 0:
            print "light toggle"
        elif commandlist[0] == "on":
            print "lights on"
        elif commandlist[0] == "off":
            print "lights off"
        elif commandlist[0] == "set":
            print "set tree"
        elif commandlist[0] == "color":
            print "color control"
        elif commandlist[0] == "dim":
            print "brightness dim"
        elif commandlist[0] == "bright":
            print "brightness high"
        elif commandlist[0] == "brightness":
            print "brightness level"
        elif commandlist[0] == "":
            print "empty command"
        else:
            print "err"    
