import tkinter as tk
import ctypes
import os
from datetime import datetime
from threading import Timer
from playsound import playsound

SCREEN_WIDTH = ctypes.windll.user32.GetSystemMetrics(0)
SCREEN_HEIGHT = ctypes.windll.user32.GetSystemMetrics(1)

APP_HEIGHT = 230
APP_WIDTH = 300
BUTTON_SIZE = 30
BACKGROUND ='white'

SUNDAY = 6

week = 0
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

def increase_one_day(canvas, days_with_no_check_obj, check_per_week_obj):
    global days
    global week

    days = days + 1
    update_object(canvas, days_with_no_check_obj, days)

    if datetime.today().weekday() == SUNDAY:
        week = 0
        update_object(canvas, check_per_week_obj, week)

    add_one_after_one_day(canvas, days_with_no_check_obj, check_per_week_obj)


def update_object(canvas, object, number):
    canvas.itemconfig(object, text=str(number).zfill(2))
    canvas.update()

def naty_check(canvas, days_with_no_check_obj, check_per_week_obj):
    global days
    global timer
    global week

    days = 0
    canvas.itemconfig(days_with_no_check_obj, text=str(days).zfill(2))
    canvas.update()
    days = -1 # Cancel the add on the day NatyCheck happen

    timer.cancel()
    timer.join()
    path = os.path.dirname(os.path.realpath(__file__))
    playsound(path + "\\audio\\naty-check.mp3")
    week = week + 1
    update_object(canvas, check_per_week_obj, week)
    add_one_after_one_day(canvas, days_with_no_check_obj, check_per_week_obj)

def add_one_after_one_day(canvas, days_with_no_check_obj, check_per_week_obj):
    global timer

    x = datetime.today()
    y = x.replace(day=x.day + 1, hour=22, minute=0, second=0, microsecond=0)
    delta_t = y - x

    secs = delta_t.seconds + 1

    timer = Timer(secs, lambda: increase_one_day(canvas, days_with_no_check_obj, check_per_week_obj))
    timer.start()

def main():
    global days
    global week

    window, canvas = create_canvas()
    font = ('Verdana', 14)

    canvas.create_text(10, 10, anchor='nw', text='   We have proudly worked ', width=APP_WIDTH, font=font,
                       fill='black', justify=tk.CENTER)
    canvas.create_text(10, 130, anchor='nw', text='   days with no Naty Checks ', font=font, width=APP_WIDTH,
                       fill='black', justify=tk.CENTER)

    font = ('Verdana', 10, 'bold')
    canvas.create_text(45, 175, anchor='nw', text=' Naty Checks in the current week',
                       font=font, width=APP_WIDTH, fill='black', justify=tk.CENTER)

    font = ('Verdana', 50)
    days_with_no_check_obj = canvas.create_text(110, 40, anchor='nw', text=str(days).zfill(2), width=APP_WIDTH,
                              font=font, fill='green', justify=tk.CENTER)

    font = ('Verdana', 10, 'bold')
    check_per_week_obj = canvas.create_text(25, 175, anchor='nw', text=str(week).zfill(2), font=font, width=APP_WIDTH,
                       fill='red', justify=tk.CENTER)

    check = tk.Button(window, text='NATY CHECK', width=BUTTON_SIZE,
                      command=lambda: naty_check(canvas, days_with_no_check_obj, check_per_week_obj),
                      background='red', foreground='white', font=('Verdana', 14, 'bold'))

    check.pack()

    add_one_after_one_day(canvas, days_with_no_check_obj, check_per_week_obj)
    #reset_week_every_sunday()

    window.mainloop()

if __name__ == '__main__':
    main()