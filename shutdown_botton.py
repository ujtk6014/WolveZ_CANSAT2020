##シャットダウンボタンを押したらシャットダウンコードが実行される
##ラズパイ側で起動時に自動実行の設定する必要有
##詳細は参考サイト参照

import time
import RPi.GPIO as GPIO
import os
import constant as ct

GPIO.setmode(GPIO.BCM)

GPIO.setup(ct.const.SHUTDOWN,GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        GPIO.wait_for_edge(ct.const.SHUTDOWN, GPIO.FALLING)
        sw_counter = 0

        while True:
            sw_status = GPIO.input(ct.const.SHUTDOWN)

            if sw_status == 0:
                sw_counter = sw_counter + 1
                if sw_counter >= 200: #2秒以上押し続けるとshutdownコマンド実行
                    os.system("sudo shutdown -h now")
                    break
            else:
                break

            time.sleep(0.01)

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()