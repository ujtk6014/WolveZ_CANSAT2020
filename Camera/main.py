import cansat
from time import sleep

can=cansat.Cansat()
can.setup()

try:
    while True:
        can.sensor()
        sleep(0.1)
        can.sequence()
        sleep(0.1)
except KeyboardInterrupt:
    print('finished')
    pass
