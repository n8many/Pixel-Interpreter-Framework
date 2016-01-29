import serial
from interp import Interp

ser = serial.Serial("/dev/ttyAMA0", 115200)

while True:
    out = ''
    while ser.inWaiting()>0:
        out += ser.read(1)
    if out != '':
        if out == "ON\r\n":
            print "LIGHTS ON"
            Interp("lights on")

        elif out == "OFF\r\n":
            print "LIGHTS OFF"
            Interp("lights off")

        elif out == "A\r\n":
            print "TOGGLE"
            Interp("lights")
        else:
            print repr(out) 

