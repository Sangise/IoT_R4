import RPi.GPIO as GPIO
from time import sleep

#ポート番号の定義
SWITCH = 24
LED = 25
led_value = GPIO.LOW

#GPIOの初期化
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def my_callback(ch):
	global led_value
	if ch == SWITCH:
		led_value = not led_value
		if led_value == GPIO.HIGH:
			GPIO.output(LED, GPIO.HIGH)
			print("LED ON")
		else:
			GPIO.output(LED, GPIO.LOW)
			print("LED OFF")

#イベントの設定
GPIO.add_event_detect(SWITCH, GPIO.RISING, callback=my_callback, bouncetime=200)


try:
	while True:
		sleep(0.01)
		
except KeyboardInterrupt:
	pass
	
GPIO.cleanup()