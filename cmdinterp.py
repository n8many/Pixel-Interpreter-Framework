from interp import Interp

a = Interp()
while True:
    s = raw_input('---> ')
    if s != 'end':
        a.interpret(s)
    else:
        break
    
