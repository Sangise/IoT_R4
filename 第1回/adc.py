import RPi.GPIO as GPIO
from time import sleep

def readadc(adcnum, clockpin, mosipin, misopin, cspin):
	if adcnum > 7 or adcnum < 0:
		return -1
	GPIO.output(cspin, GPIO.HIGH)
	GPIO.output(clockpin, GPIO.LOW)
	GPIO.output(cspin, GPIO.LOW)

	commandout = adcnum
	commandout = commandout | 0x18
	commandout = commandout << 3

	for i in range(5):
		if commandout & 0x80 == 0x80:
			GPIO.output(mosipin, GPIO.HIGH)
		else:
			GPIO.output(mosipin, GPIO.LOW)
		commandout = commandout << 1
		GPIO.output(clockpin, GPIO.HIGH)
		GPIO.output(clockpin, GPIO.LOW)

	adcout = 0
	for i in range(13):
		GPIO.output(clockpin, GPIO.HIGH)
		GPIO.output(clockpin, GPIO.LOW)
		adcout = adcout << 1
		if i > 0 and GPIO.input(misopin) == GPIO.HIGH:
			adcout = adcout | 0x1

	GPIO.output(cspin, GPIO.HIGH)
	return adcout

GPIO.setmode(GPIO.BCM)
SPICLK = 11
SPIMOSI = 10
SPIMISO = 9
SPICS = 8

GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICS, GPIO.OUT)

try:
	while True:
		inputVal0 = readadc(0, SPICLK, SPIMOSI, SPIMISO, SPICS)
		print("ADC = "+ str(inputVal0))
		sleep(1.0)

except KeyboardInterrupt:
	pass

GPIO.cleanup()