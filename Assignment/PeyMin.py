from tkinter import *
from tkinter import ttk,messagebox
import time
from datetime import *
from datetime import datetime
import os
import pygame 
 

# Initialize the pygame mixer 
pygame.mixer.init() 

window = Tk()
window.title("Alarm")
window.config(background="#cdf7f3")

title_label = Label(window, text="Alarm Application\nWelcome! Feel free to set an alarm!", font=("Comic Sans MS", 16, "bold"), bg="#f5e2cb")
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

    record.append({"alarm_time": set_alarm,
        "note": user_note,
        "active": True,
        "date": current_date,
        "day": today_day})
    
    list_record.insert(END, f"Alarm: {set_alarm} | Note: {user_note} | Date: {current_date} | Day: {today_day}")
    messagebox.showinfo("Succes", "You have save succesfully")

    


def check_alarm():
    """Check all saved alarms and trigger them if the current time matches."""
    current_time = datetime.now().strftime("%I:%M %p")
    for i, alarm in enumerate(record[:]):
        if alarm["active"] and alarm["alarm_time"] == current_time:
            pygame.mixer.music.load("C:/Users/wongp/Music/morning_flower.mp3")  # Replace with your file path
            pygame.mixer.music.play(-1)
            
        
            # Create the alarm notification window
            alarm_window = Toplevel(window)
            alarm_window.title("Alarm Notification")
            alarm_window.geometry("300x200")

            # Display the alarm message
            alarm_message = Label(alarm_window, text=f"ALARM! It's {alarm['alarm_time']}\nNote: {alarm['note']}", font=("Arial", 14), fg="red")
            alarm_message.pack(pady=20)

            def dismiss_alarm():
                 pygame.mixer.music.stop()
                 alarm_window.destroy()  # Close the alarm window
                 alarm["active"] = False  # Mark this alarm as dismissed

            def snooze_alarm():
                pygame.mixer.music.stop() 
                if record:  # Check if there's an alarm in the list
                    snooze_time = datetime.now() + timedelta(minutes=5)  # Add 5 minutes to the current time
                    snoozed_alarm = snooze_time.strftime("%I:%M %p")  # Format it in the same way
                    user_note = alarm["note"]  # Retain the same note for the snoozed alarm

                    # Update the alarm in the list (replace the last saved alarm)
                    record[i] = {"alarm_time": snoozed_alarm, "note": user_note, "active": True,"date": alarm["date"],"day": alarm["date"]}
                    list_record.delete(i)
                    list_record.insert(i, f"Alarm: {snoozed_alarm} | Note: {record[i]['note']} | Date: {record[i]['date']} | Day: {record[i]['day']}")

                    # Optionally: Update the alarm label on the UI
                    label_alarm.config(text=f"Snoozed! New time: {snoozed_alarm} \n Note: {user_note}", font=("Arial", 15), fg="blue")
                    label_alarm.grid(row=5, column=0, columnspan=3, pady=10)
                    
                    print(f" New time: {snoozed_alarm}, Note: {user_note}")
                    alarm["active"] = True
                    messagebox.showinfo("Succes", "You have snooze succesfully")
                    
                    
                    # Ensure that the alarm checks again after the snooze time
                    window.after(300000,check_alarm)

            # Add buttons for dismissing or snoozing the alarm
            dismiss_button = Button(alarm_window, text="Dismiss", command=dismiss_alarm, font=("Arial", 12))
            dismiss_button.pack(pady=10)

            snooze_button = Button(alarm_window, text="Snooze", command=snooze_alarm, font=("Arial", 12))
            snooze_button.pack(pady=10)

            print(f"ALARM! Time to wake up! Alarm: {alarm['alarm_time']}, Note: {alarm['note']}")
            alarm["active"] = False  # Mark this alarm as triggered
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
        messagebox.showerror("Error", "Please save an alarm before starting!")  # Show error message if no alarm is saved
    else:
        messagebox.showinfo("Succes", "You have turn on succesfully")
        print("Starting alarm...")
        
        # Continue with starting the alarm if it is saved

def delete_alarm():
    selected_alarm =list_record.curselection()
    if not selected_alarm:
        messagebox.showerror("Error","Please select a alarm before delete")
        return
    
    index = selected_alarm[0]
    list_record.delete(index)

    del record[index]
    messagebox.showinfo("Deleted", "Alarm deleted successfully.")


time_label = Label(window, text="")
date_label = Label(window, text="")

list_record = Listbox(window, width=60, height=20)
list_record.grid(row=6, column=0, columnspan=3)

# BUTTONS
save = Button(window, text="Save", command=alarm_record, font=("Arial", 10, "bold"))
save.grid(row=4, column=0, columnspan=2)

turn_on = Button(window, text="Turn on", command=start_alarm, font=("Arial", 10, "bold"))
turn_on.grid(row=4, column=1, pady=10)

delete = Button(window, text="Delete",command=delete_alarm ,font=("Arial", 10, "bold"))
delete.grid(row=4, column=2, pady=10)

label_msg = Label(window, text="Note: ", font=("Arial", 15), background="lightblue")
label_msg.grid(row=3, column=0)

msg = Entry(window, width=30)
msg.grid(row=3, column=0, columnspan=3, pady=20)

label_alarm = Label(window, text="", font=("Arial", 15))
label_alarm.grid(row=6, column=0)


instruction_msg = Label(window, text="*After you select the time, remember to save then proceed to press Turn on.",font=("Arial", 10, "bold"), fg="red")
instruction_msg.grid(row=4, column=3, columnspan=7)



check_alarm()
display_time()
window.mainloop()
