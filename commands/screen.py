from commands.command import Command
import RPi.GPIO

class Screen(Command):
    def __init__(self, credentials):
        print 'Loading screen module'
        self.keywords = ['screen', 'display', 'mirror']
        RPi.GPIO.setwarnings(False)
        RPi.GPIO.setmode(RPi.GPIO.BOARD)
        self.pin = credentials['pin']
        RPi.GPIO.setup(self.pin, RPi.GPIO.OUT)
        RPi.GPIO.setwarnings(True)
        self.isOn = False
        self.getStatus()
        
    def getStatus(self):
        self.isOn = not RPi.GPIO.input(self.pin)

    def run(self, commandlist):
        self.getStatus()
        if len(commandlist) == 0:
            self.isOn = ~self.isOn
            print 'screen toggle'

        for i in xrange(0, len(commandlist)):
            if len(commandlist) == 1:
                self.isOn = not self.isOn
                print 'screem toggle'
                break
            
            if commandlist[i] == "on":
                self.isOn = True 
                print 'screen on'
                
            elif commandlist[i] == "off":
                self.isOn = False
                print 'screen off'
                
            else:
                pass
        RPi.GPIO.output(self.pin, not self.isOn)
