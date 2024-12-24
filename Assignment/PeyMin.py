from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import time
from datetime import *
from datetime import datetime
import os

window = Tk()
window.title("Alarm")
window.config(background="#cdf7f3")

title_label = Label(window, text="Welcome! Feel free to set an alarm!", font=("Comic Sans MS", 16, "bold"), bg="#f5e2cb")
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

def save_error_msg():
    # Show an error message using messagebox.showerror
    messagebox.showerror("Error", "Please save an alarm before starting!")

def save_succes_msg():
    messagebox.showinfo("Congratulation!!", "You have save succesfully")

def alarm_record():
    user_note = msg.get()
    set_alarm = f"{hour.get()}:{min.get()} {AM_PM.get()}"
    current_date = datetime.now().strftime("%b %d, %Y")
    today_day = datetime.now().strftime("%A")

    record.append((set_alarm, user_note, current_date, today_day))
    list_record.insert(END, f"Alarm: {set_alarm} | Note: {user_note} | Date: {current_date} | Day: {today_day}")

    Label_alarm.config(text=f"Alarm saved: {set_alarm} \n Note: {user_note}", font=("Arial", 15), fg="green")
    Label_alarm.grid(row=5, column=0, columnspan=5, pady=10)
   
    save_succes_msg()

def check_alarm():
    """Check all saved alarms and trigger them if the current time matches."""
    current_time = datetime.now().strftime("%I:%M %p")
    for i, (alarm_time, note, _, _) in enumerate(record[:]):
        if alarm_time == current_time:
            # Create the alarm notification window
            alarm_window = Toplevel(window)
            alarm_window.title("Alarm Notification")
            alarm_window.geometry("300x200")

            # Display the alarm message
            alarm_message = Label(alarm_window, text=f"ALARM! It's {alarm_time}\nNote: {note}", font=("Arial", 14), fg="red")
            alarm_message.pack(pady=20)

            def dismiss_alarm():
                alarm_window.destroy()  # Close the alarm window

            def snooze_alarm():
                if record:  # Check if there's an alarm in the list
                    snooze_time = datetime.now() + timedelta(minutes=5)  # Add 5 minutes to the current time
                    snoozed_alarm = snooze_time.strftime("%I:%M %p")  # Format it in the same way
                    user_note = record[-1][1]  # Retain the same note for the snoozed alarm

                    # Update the alarm in the list (replace the last saved alarm)
                    record[-1] = (snoozed_alarm, user_note, record[-1][2], record[-1][3])

                    # Optionally: Update the alarm label on the UI
                    Label_alarm.config(text=f"Snoozed! New time: {snoozed_alarm} \n Note: {user_note}", font=("Arial", 15), fg="blue")
                    Label_alarm.grid(row=5, column=0, columnspan=3, pady=10)
                    
                    print(f"Snoozed alarm! New time: {snoozed_alarm}, Note: {user_note}")

            # Add buttons for dismissing or snoozing the alarm
            dismiss_button = Button(alarm_window, text="Dismiss", command=dismiss_alarm, font=("Arial", 12))
            dismiss_button.pack(pady=10)

            snooze_button = Button(alarm_window, text="Snooze", command=snooze_alarm, font=("Arial", 12))
            snooze_button.pack(pady=10)

            print(f"ALARM! Time to wake up! Alarm: {alarm_time}, Note: {note}")
            Label_alarm.config(text=f"ALARM! {alarm_time}: {note}", fg="orange")
            del record[i]
            break

    window.after(1000, check_alarm) 

def display_time():
    """Updates the current time displayed on the front page."""
    current_time = datetime.now().strftime("%I:%M:%S %p")
    current_date = datetime.now().strftime("%b %d, %Y")

    time_label.config(text=current_time, font=("Comic Sans MS", 20), fg="blue")
    time_label.grid(row=0, column=5)
    window.after(1000, display_time)

    date_label.config(text=current_date, font=("Comic Sans MS", 20), fg="blue")
    date_label.grid(row=1, column=5)




def start_alarm():
    """Start the alarm, but only if an alarm is saved."""
    if not record:  # Check if the record list is empty
        save_error_msg()  # Show error message if no alarm is saved
    else:
        print("Starting alarm...")
        # Continue with starting the alarm if it is saved (you can put your alarm logic here)

time_label = Label(window, text="")
date_label = Label(window, text="")

list_record = Listbox(window, width=60, height=20)
list_record.grid(row=6, column=0, columnspan=3)

# BUTTONS
save = Button(window, text="Save", command=alarm_record, font=("Ink Free", 10, "bold"))
save.grid(row=4, column=0, columnspan=2)

Turn_on = Button(window, text="Turn_on", command=start_alarm, font=("Ink Free", 10, "bold"))
Turn_on.grid(row=4, column=1, pady=10, columnspan=2)

delete = Button(window, text="Turn_on", command=start_alarm, font=("Ink Free", 10, "bold"))
delete.grid(row=4, column=1, pady=10, columnspan=2)

label_msg = Label(window, text="Note: ", font=("Arial", 15), background="lightblue")
label_msg.grid(row=3, column=0)

msg = Entry(window, width=30)
msg.grid(row=3, column=0, columnspan=3, pady=20)

Label_alarm = Label(window, text="", font=("Arial", 15))
Label_alarm.grid(row=6, column=0)

check_alarm()
display_time()
window.mainloop()
