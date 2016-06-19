import time
import serial
from interp import Interp

ser = serial.Serial("/dev/ttyAMA0", 115200)

print "Reading from Teensy"

while True: 
    out = ''
    try:
        n = ser.inWaiting()
        if n > 0:
            out = ser.read()
    except:
        print "Could not read"
    if out != '' and out != '\n':
        if out == "N":
            print "LIGHTS ON"
            Interp("lights on")

        elif out == "F":
            print "LIGHTS OFF"
            Interp("lights off")

        elif out == "A":
            print "TOGGLE"
            Interp("lights")
        else:
            print "Unrecognized command" 

