#FileName <hellotkinter3.py>
#-*- conding: utf-8 -*-

import tkinter as tk # tkinter の読み込み
import RPi.GPIO as GPIO
from time import sleep
import threading

win = tk.Tk() # ウインド(win)を作成
win.title("LED_ON/OFF") # タイトルの設定
win.geometry("500x300") # ウインドの大きさを500x300に設定
Entry_box = tk.Entry(width = 20)
Entry_box.place(x = 50, y = 10)

global flag
global inputval0
flag = 0
inputval0=0

GPIO.setmode(GPIO.BCM)
SPICLK = 11
SPIMOSI = 10
SPIMISO = 9
SPICS = 8

GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICS, GPIO.OUT)

def ADC_ON(): # ボタンを押したときにADCをスタートし、flagを1に。
    global flag
    flag = 1
    threading1 = threading.Thread(target=adc_get)
    threading1.start() 

def ADC_OFF(): # ボタンを押すとflagを2に。
    global flag
    flag = 2
    #threading1 = threading.Thread(target=adc_get)

def adc_get(): # ADCから取得したデータをEntry_boxに表示
    global flag
    global inputval0
    while flag==1:
        inputval0 = readadc(0, SPICLK, SPIMOSI, SPIMISO, SPICS)
        value = str(inputval0)
        Entry_box.delete(0, tk.END)
        Entry_box.insert(tk.END,value)
        sleep(1.0)

    value = ""
    Entry_box.insert(tk.END,value)
    Entry_box.delete(0, tk.END)
    
def readadc(adcnum, clockpin, mosipin, misopin, cspin): # ADC読み取り
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


    

# ボタン（変数名：Button）の作成
Button_ON = tk.Button(win,width=5, background="orange", text="スタート", command = ADC_ON)
Button_ON.place(x = 300, y = 5)
Button_OFF = tk.Button(win,width=5, background="aqua", text="ストップ", command = ADC_OFF)
Button_OFF.place(x = 380, y = 5)




win.mainloop() # ウインドを動かすためのおまじない

GPIO.cleanup()