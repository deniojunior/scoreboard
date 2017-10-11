import tkinter as tk
import ctypes
import os
from datetime import datetime
from threading import Timer
from playsound import playsound

SCREEN_WIDTH = ctypes.windll.user32.GetSystemMetrics(0)
SCREEN_HEIGHT = ctypes.windll.user32.GetSystemMetrics(1)

APP_HEIGHT = 200
APP_WIDTH = 300
BUTTON_SIZE = 30
BACKGROUND ='white'
NUMBER_SPACE = '    '

ONE_DAY = 1000*60*60#*24

days = 0
timer = 0

def create_canvas():
    window = tk.Tk()
    window.overrideredirect(True)
    window.configure(background=BACKGROUND, highlightbackground=BACKGROUND)
    window.geometry(str(APP_WIDTH) + 'x' + str(APP_HEIGHT) + '+' + str(SCREEN_WIDTH-APP_WIDTH) + '+0')
    canvas = tk.Canvas(window, height=APP_HEIGHT-BUTTON_SIZE, width=SCREEN_WIDTH, bg=BACKGROUND)
    canvas.pack()
    
    return (window, canvas)

def add_one(canvas, text):
    global days

    days = days + 1
    canvas.itemconfig(text, text=NUMBER_SPACE+str(days).zfill(2))
    canvas.update()

def naty_check(canvas, text):
    global days
    global timer

    days = 0
    canvas.itemconfig(text, text=NUMBER_SPACE+str(days).zfill(2))
    canvas.update()

    timer.cancel()
    timer.join()
    path = os.path.dirname(os.path.realpath(__file__))
    print(path)
    playsound(path + "\\audio\\naty-check.mp3")
    add_one_after_onde_day(canvas, text)

def add_one_after_onde_day(canvas, text):
    global timer

    x = datetime.today()
    y = x.replace(day=x.day + 1, hour=22, minute=0, second=0, microsecond=0)
    delta_t = y - x

    secs = delta_t.seconds + 1

    timer = Timer(secs, lambda: add_one(canvas, text))
    timer.start()
    
def main():
    global days

    window, canvas = create_canvas()
    font = ('Verdana', 14)
    canvas.create_text(10, 10, anchor='nw', text='   We have proudly worked ', width=APP_WIDTH, font=font, fill='black', justify=tk.CENTER)
    canvas.create_text(10, 130, anchor='nw', text='   days with no Naty Checks ', font=font, width=APP_WIDTH, fill='black', justify=tk.CENTER)
    button = tk.Button(window, text='NATY CHECK', width=BUTTON_SIZE, command=lambda: naty_check(canvas, text), background='red', foreground='white', font=('Verdana', 14, 'bold'))
    button.pack()

    font = ('Verdana', 50)
    text = canvas.create_text(10, 40, anchor='nw', text=NUMBER_SPACE+str(days).zfill(2), width=APP_WIDTH, font=font, fill='green', justify=tk.CENTER)

    add_one_after_onde_day(canvas, text)

    window.mainloop()

if __name__ == '__main__':
    main()