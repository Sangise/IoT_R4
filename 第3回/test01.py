from time import sleep
import board
import adafruit_dht

while True:
    try:
        temperature = adafruit_dht.DHT22(board.D14, use_pulseio=False).temperature
        humidity = adafruit_dht.DHT22(board.D14, use_pulseio=False).humidity
        print("Temp: {:.1f} C    Humidity: {:.1f}% "
            .format(temperature, humidity))
    except:
        continue

    sleep(1.0)

