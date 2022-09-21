#FileName <hellotkinter3.py>
#-*- conding: utf-8 -*-

import tkinter as tk # tkinter の読み込み
import threading
#import Adafruit_DHT #DTHの読み込み
import adafruit_dht
from time import sleep
import board

win = tk.Tk() # ウインド(win)を作成
win.title("LED_ON/OFF") # タイトルの設定
win.geometry("500x300") # ウインドの大きさを500x300に設定
Entry_box = tk.Entry(width = 20)
Entry_box.place(x = 50, y = 10)
Entry_box2 = tk.Entry(width = 20)
Entry_box2.place(x = 50, y = 40)

global flag
global inputval0
flag = 0
inputval0=0

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
        inputval0 = readDHT()
        value = str(inputval0[0])
        value2 = str (inputval0[1])
        Entry_box.delete(0, tk.END)
        Entry_box.insert(tk.END,value)
        Entry_box2.delete(0, tk.END)
        Entry_box2.insert(tk.END,value2)
        sleep(1.0)


    value = ""
    Entry_box.insert(tk.END,value)
    Entry_box.delete(0, tk.END)
    Entry_box2.insert(tk.END,value2)
    Entry_box2.delete(0, tk.END)
    
def readDHT(): # DHT読み取り
    while True:
        try:# Print the values to the serial port
            temperature = adafruit_dht.DHT22(board.D14, use_pulseio=False).temperature
            humidity = adafruit_dht.DHT22(board.D14, use_pulseio=False).humidity
            print("Temp: {:.1f} C    Humidity: {}% ".format(temperature, humidity))
            return temperature,humidity
        except:
            continue
  
    

# ボタン（変数名：Button）の作成
Button_ON = tk.Button(win,width=5, background="orange", text="スタート", command = ADC_ON)
Button_ON.place(x = 300, y = 5)
Button_OFF = tk.Button(win,width=5, background="aqua", text="ストップ", command = ADC_OFF)
Button_OFF.place(x = 380, y = 5)


win.mainloop() # ウインドを動かすためのおまじない
