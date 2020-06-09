import ultrasonic_class

TRIGPIN=17 #定数
ECHOPIN=18 #定数

def setupUltrasonic(trigpin,echopin):
    ultrasonic_class.setmode()
    
    trig_pin=ultrasonic_class.Ultrasonic()
    trig_pin.trig_setup(trigpin)
    echo_pin=ultrasonic_class.Ultrasonic()
    echo_pin.echo_setup(echopin)

def getDistance():
    distance=ultrasonic_class.get(TRIGPIN,ECHOPIN) #値をdistanceに格納
    print ("現在の距離 ： %.3f cm"%(distance))
    return distance

#'''
try:
    setupUltrasonic(TRIGPIN,ECHOPIN)
    while True:
        ultrasonic_class.sleep(1)
        distance=getDistance()

except KeyboardInterrupt:        #例外（CTRL+Cが押された時)処理
    ultrasonic_class.end()                       #endを実行
#'''