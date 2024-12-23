from tkinter import *
from tkinter import ttk
from datetime import datetime

window = Tk()
window.geometry("800x600")
window.title("Alarm")
window.config(background="light blue")

title_label = Label(window, text="Welcome! Feel free to set an alarm!", font=("Comic Sans MS", 16, "bold"), bg="orange")
title_label.grid(row=0, column=0, columnspan=3, pady=10, sticky="ew")

style = ttk.Style()
style.configure("TCombobox", font=("Arial", 14), padding=10)

hour = ttk.Combobox(window, width=10, style="TCombobox", state="readonly")
hour["value"] = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
hour.current(0)
hour.grid(row=1, column=0)

min = ttk.Combobox(window, width=10, style="TCombobox", state="readonly")
min["value"] = [f"{i:02}" for i in range(0, 60)]
min.current(0)
min.grid(row=1, column=1)

AM_PM = ttk.Combobox(window, width=10, style="TCombobox", state="readonly")
AM_PM["value"] = ["AM", "PM"]
AM_PM.current(0)
AM_PM.grid(row=1, column=2)

record = []

def alarm_record():
    user_note = msg.get()
    set_alarm = f"{hour.get()}:{min.get()} {AM_PM.get()}"
    current_date = datetime.now().strftime("%b %d, %Y")
    today_day = datetime.now().strftime("%A")

    record.append((set_alarm, user_note, current_date, today_day))
    list_record.insert(END, f"Alarm: {set_alarm} | Note: {user_note} | Date: {current_date} | Day: {today_day}")

    Label_alarm.config(text=f"Alarm saved: {set_alarm} \n Note: {user_note}", font=("Arial", 20), fg="green")
    Label_alarm.grid(row=4, column=0, columnspan=3, pady=10)
    print(f"Alarm saved for: {set_alarm}")
    print(f"Note: {user_note}")

def check_alarm():
    
    current_time = datetime.now().strftime("%I:%M %p")
    for alarm_time, note, _, _ in record:
        if alarm_time == current_time:
            print(f"ALARM! Time to wake up! Alarm: {alarm_time}, Note: {note}")
            Label_alarm.config(text=f"ALARM! {alarm_time}: {note}", fg="orange")
    window.after(1000, check_alarm)

def display_time():
    
    current_time = datetime.now().strftime("%I:%M:%S %p")
    current_date = datetime.now().strftime("%b %d, %Y")

    time_label.config(text=current_time, font=("Comic Sans MS", 20), fg="blue")
    time_label.grid(row=0, column=5)
    window.after(1000, display_time)

    date_label.config(text=current_date, font=("Comic Sans MS", 20), fg="blue")
    date_label.grid(row=1, column=5)

time_label = Label(window, text="")
date_label = Label(window, text="")

button = Button(window, text="Save", command=alarm_record)
button.config(font=("Ink Free", 10, "bold"))
button.grid(row=1, column=3)

snooze = Button(window, text="Snooze")
snooze.config(font=("Ink Free", 10, "bold"))
snooze.grid(row=3, column=3, pady=10)

add = Button(window, text="Start", command=check_alarm)
add.config(font=("Ink Free", 10, "bold"))
add.grid(row=5, column=3, pady=10)

label_msg = Label(window, text="Note: ", font=("Arial", 15), background="lightblue")
label_msg.grid(row=3, column=0)

msg = Entry(window, width=30)
msg.grid(row=3, column=0, columnspan=3, pady=20)

Label_alarm = Label(window, text="", font=("Arial", 15))
Label_alarm.grid(row=5, column=0)

list_record = Listbox(window, width=60, height=20)
list_record.grid(row=6, column=0, columnspan=3)

display_time()
window.mainloop()
