import cansat
from time import sleep

can=cansat.Cansat()

try:
    while True:
        can.sequence()
        sleep(0.1)
except KeyboardInterrupt:
    print('finished')
    pass
