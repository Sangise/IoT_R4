#FileName <hellotkinter3.py>
#-*- conding: utf-8 -*-

import tkinter as tk # tkinter の読み込み
import RPi.GPIO as GPIO

win = tk.Tk() # ウインド(win)を作成
win.title("LED_ON/OFF") # タイトルの設定
win.geometry("500x300") # ウインドの大きさを500x300に設定
GPIO.setmode(GPIO.BCM)
GPIO.setup(25,GPIO.OUT)


def LED_ON(): # ボタンを押したときにLEDを点灯する。
    GPIO.output(25, GPIO.HIGH)

def LED_OFF():
    GPIO.output(25, GPIO.LOW)
    

# ボタン（変数名：Button）の作成
Button_ON = tk.Button(win,width=5, background="orange", text="スタート", command = LED_ON)
Button_ON.place(x = 300, y = 5)
Button_OFF = tk.Button(win,width=5, background="aqua", text="ストップ", command = LED_OFF)
Button_OFF.place(x = 380, y = 5)

try:
    win.mainloop() # ウインドを動かすためのおまじない
finally:
    GPIO.cleanup()
    
#GUI