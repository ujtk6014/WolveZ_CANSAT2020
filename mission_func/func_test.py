import func_test_class as test
from time import sleep

cansat = test.simpleFunc()

try:
    while True:
        cansat.sensor()
        sleep(0.1)
        cansat.sequence()
        sleep(0.1)
except KeyboardInterrupt:
    print('test has been stopped manually')
    pass
    
