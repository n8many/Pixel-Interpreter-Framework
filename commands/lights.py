from commands.command import Command
from beautifulhue.api import Bridge

class Lights(Command):
    def __init__(self, credentials):
        print 'Loading lights module'
        self.keywords = ['light', 'lights']
        self.bridge = Bridge(device={'ip':credentials['ip']},
                user={'name':credentials['u']})
        self.groups = credentials['groups']
        self.defaults = credentials['default']
        self.currentGroup = self.groups[self.defaults['group']] 
        self.colors = credentials['color']
        self.isOn = False
        self.status = dict()
        self.getStatus()

    def sendCommand(self, group, setting):
        print setting
        for light in group:
            resource = {'which':light,'data':{'state':setting}}
            try: 
                self.bridge.light.update(resource)
            except:
                print "Cannot connect to bridge"

    def getStatus(self):
        self.isOn = False
        for light in self.currentGroup:
            resource = {'which':light}
            try:    
                self.status[light] = self.bridge.light.get({'which':light})['resource']
                if self.status[light]['state']['on']:
                    self.isOn = True
            except:
                print "Cannot Connect to light " + str(light)


    def run(self, commandlist):
        self.getStatus()
        data = {"on":True}
        group = self.currentGroup
        if len(commandlist) == 0:
            data['on'] = ~self.isOn
            if data['on'] == False:
                group = self.groups['all']
            print "light toggle"

        for i in xrange(0, len(commandlist)):
            if len(commandlist) == 1:
                data['on'] = not self.isOn
                print "light toggle"
                break
            
            if commandlist[i] == 'light' and self.isNumber(commandlist[i+1]):
                group = [int(commandlist[i+1])]

            elif commandlist[i] in self.groups:
                self.currentGroup = self.groups[commandlist[i]]
                print 'group ' + commandlist[i]
            
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
                    data = dict(data.items()+self.colors[commandlist[i+1]].items())
                    print "set color" + commandlist[i+1]
                    
            elif commandlist[i] == "dim":
                data['bri'] = 50
                print "brightness dim"

            elif commandlist[i] == "bright":
                data['bri'] = 255
                print "brightness high"

            elif commandlist[i] == "brightness" and self.isNumber(commandlist[i+1]):
                data['bri'] = int(commandlist[i+1]) * 25 + 5            
                print "brightness level " + commandlist[i+1] 

            elif commandlist[i] == 'soft':
                data['sat'] = 100
                print "lighten color"

            elif commandlist[i] == 'deep':
                data['sat'] = 255
                print "deepen color"

            else:
                pass

        self.sendCommand(group,data)
