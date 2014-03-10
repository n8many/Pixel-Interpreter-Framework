from commands.command import Command
from beautifulhue.api import Bridge

class Lights(Command):
    def __init__(self, credentials):
        self.keywords = ['light','lights']
#       self.bridge = Bridge(device={'ip':credentials['ip']},
#                user={'name':credentials['u']})
        self.groups = credentials['groups']
        self.currentGroup = self.groups['all']


    def sendCommand(self, group, setting):
        for light in group:
            resource = {'which':light,'data':{setting}}
            bridge.light.update(resource)

    def isNumber(self, word):
        try:
            int(word)
            return True
        except:
            return False

    def run(self, commandlist):
#        self.getStatus()
        data = {"on":True}
        group = self.currentGroup
        for i in xrange(0, len(commandlist)-1):
            if len(commandlist) == 0:
                print "light toggle"
                break
            
            if commandlist[i] == 'light' and self.isNumber(commandlist[i+1]):
                group = [int(commandlist[i+1])]

            elif commandlist[i] in self.groups:
                self.currentGroup = self.groups[commandlist[i]]
            
            elif commandlist[i] in self.colors:
                pass
            
            elif self.isNumber(commandlist[i]):
                pass

            elif commandlist[i] == "on":
                data['on'] = True
                print "lights on"
                
            elif commandlist[i] == "off":
                data['on'] = False
                print "lights off"
                
            elif commandlist[i] == "set":
                print "set tree"
                
            elif commandlist[i] == "color":
                if commandlist[i+1] in self.colors:
                    data = dict(data.items()+self.colors[i+1].items())
                    print "set color" + commandlist[i+1]
                    
            elif commandlist[0] == "dim":
                data['bri'] = 50
                print "brightness dim"

            elif commandlist[i] == "bright":
                data['bri'] = 255
                print "brightness high"

            elif commandlist[i] == "brightness" and self.isNumber(commandlist[i+1]):
                data['bri'] = int(commandlist[1])*25 + 5            
                print "brightness level"

            elif commandlist[i] == 'soft':
                data['sat'] = 100
                print "lighten color"

            elif commandlist[i] == 'deep':
                data['sat'] = 255
                print "deepen color"

            else:
                pass

#            self.sendCommand(group,data)
