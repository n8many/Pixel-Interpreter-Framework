from interp import Interp

endcommands = ['end','exit','quit','stop']
while True:
    s = raw_input('---> ')
    if s not in endcommands:
        Interp(s)
    else:
        break

