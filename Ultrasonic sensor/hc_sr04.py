import hc_sr04_class

hc_sr04_class.setmode()

trig_pin=hc_sr04_class.Ultrasonic()
trig_pin.trig_setup(17)
echo_pin=hc_sr04_class.Ultrasonic()
echo_pin.echo_setup(18)

try:
    hc_sr04_class.loop()                      #loopを実行
except KeyboardInterrupt:       #例外（CTRL+Cが押された時)処理
    hc_sr04_class.end()                       #endを実行