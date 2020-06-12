import time
import gps 

gps = gps.GPS()
#file kakikomi
#G = gps.GPS() #self
gps.setupGPS()
start_time = time.time()

while True:
    gps.gpsread()
    timer = 1000*(time.time() - start_time)
    timer = int(timer)
    datalog = str(timer) + ","\
              + str(gps.Time) + ","\
              + str(gps.Lat) + ","\
              + str(gps.Lon)
    
    with open("test.txt",mode = 'a') as test:
        test.write(datalog + '\n')