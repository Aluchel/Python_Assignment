import tkinter as tk
from tkinter import messagebox
import csv

class CountdownTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Countdown Timer")
        self.time_left = 0
        self.selected_note = None  #Store the selected note and time

        #Frame to hold other frames
        self.mainframe = tk.Frame(self.root, bg="#DCFFD1", relief="groove", bd=4)
        self.mainframe.pack(fill="both", expand=True, padx=3, pady=3)

        #Top Frame
        self.frame0 = tk.Frame(self.mainframe, bg="#FFD1DC", padx=20, relief="groove", bd=2)
        self.frame0.grid(row=0, column=0, columnspan=3, sticky="ew", padx=10, pady=2)
        #Lower Frames
        self.frame1 = tk.Frame(self.mainframe, bg="#D1DCFF", padx=20, width=360, relief="groove", bd=4)
        self.frame1.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.frame2 = tk.Frame(self.mainframe, bg="#A2D991", relief="groove", bd=2)
        self.frame2.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        self.frame3 = tk.Frame(self.mainframe, bg="#D1DCFF", relief="groove", bd=4)
        self.frame3.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)

        # Configure row and column expansion
        self.mainframe.grid_columnconfigure(0, weight=1)
        self.mainframe.grid_columnconfigure(1, weight=1)
        self.mainframe.grid_columnconfigure(2, weight=1)

        # Items on the tkinter window
        self.notify_label = tk.Label(self.frame0, text="TIMER APPLICATION", font=("Times New Roman",20,"bold"), bg="#FFD1DC")
        self.notify_label.pack()
        self.time_label = tk.Label(self.frame3, text="Set Time (in minutes):", font=("Times New Roman",20), bg="#D1DCFF") 
        self.time_label.grid(row=1, column=0, padx=5, pady=5)

        self.time_entry = tk.Entry(self.frame3, font=(20), relief="flat", bd=4)
        self.time_entry.grid(row=2, column=0, padx=10, pady=5)
        self.minornote=tk.Label(self.frame3, text="**Unselect the saved timer to run custom timer", font=("Times New Roman",16), bg="#D1DCFF")
        self.minornote.grid(row=3, column=0, padx=5, pady=5)
        self.minornote2=tk.Label(self.frame3, text="**Press start button multiple times to run multiple timers", font=("Times New Roman",16), bg="#D1DCFF")
        self.minornote2.grid(row=4, column=0, padx=5, pady=5)

        #Run the function to load csv data
        self.load_csv()

        #control buttons
        self.start_button = tk.Button(self.frame2, text="Start", font=("Times New Roman",20), command=self.start_timer, width=15, relief="raised", bd=4)
        self.start_button.grid(row=0, column=0, padx=5, pady=5)
        #save a new timer
        self.save_button = tk.Button(self.frame2, text="Save Timer", font=("Times New Roman",20), command=self.save_timer, width=15, relief="raised", bd=4)
        self.save_button.grid(row=1, column=0, padx=5, pady=5)
        #remove the selected timer
        self.remove_button = tk.Button(self.frame2, text="Remove Timer", font=("Times New Roman",20), command=self.remove_timer, width=15, relief="raised", bd=4)
        self.remove_button.grid(row=2, column=0, padx=5, pady=5)
        #remove selection of timer
        self.remove_button = tk.Button(self.frame2, text="Unselect Timer", font=("Times New Roman",20), command=self.unselect, width=15, relief="raised", bd=4)
        self.remove_button.grid(row=3, column=0, padx=5, pady=5)
        #Exit button
        self.exit_button=tk.Button(self.frame2, text="Exit", font=("Times New Roman",20), command=self.root.destroy, width=15, relief="raised", bd=4)
        self.exit_button.grid(row=4, column=0, padx=5, pady=5)

    def load_csv(self):
        #Load csv file data
        try:
            with open('timer.csv', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                self.csv_data = list(reader)

                self.listbox_frame = tk.Frame(self.frame1, relief="flat", bd=4)
                self.listbox_frame.pack(padx=5, pady=5)

                #Create the Scrollbar 
                scrollbar = tk.Scrollbar(self.listbox_frame, orient="vertical", relief="flat", bd=4)

                #Create the Listbox 
                self.listbox = tk.Listbox(self.listbox_frame, height=10, width=25, font=("Times New Roman",20), yscrollcommand=scrollbar.set, relief = "sunken", bd=2)

                #Insert csv file data
                for row in self.csv_data[1:]:  #Skip the header
                    self.listbox.insert(tk.END, f" {row[0]} - {row[1]} min")
                    #tk.end tells Tkinter to add the item at the end of the list.
                
                #Bind event to handle selection
                self.listbox.bind('<<ListboxSelect>>', self.on_select)

                #attach the scrollbar to the Listbox
                scrollbar.config(command=self.listbox.yview) #links to scrollbar to the lisbox on the y-axis
                scrollbar.pack(side="right", fill="y")  #makes sure the scrollbar fills up the y-axis on the right side
                self.listbox.pack(fill="both",padx=2) #only pack it after scrollbar is attached
        except FileNotFoundError:
            messagebox.showerror("File not found", "The file 'timer.csv' does not exist!")

    def on_select(self, event):
        #Handles the selection event from the listbox
        selected = self.listbox.curselection()
        if selected:
            note, minutes = self.csv_data[selected[0] + 1]  #Skip the header row
            self.selected_note = note  #store the selected note into variable
            self.time_left = int(minutes) * 60

    def unselect(self):
        if self.selected_note:
            self.listbox.selection_clear(0, tk.END)
            self.selected_note = None
            self.time_left = 0

    def start_timer(self):
        if self.selected_note is None:
            try:
                #convert the input from user into minutes
                self.time_left = int(self.time_entry.get()) * 60
            except ValueError:
                messagebox.showerror("Invalid input!", "Please enter a valid number for time!")
            else:
                TimerWindow(self.root, self.time_left, f"{int(self.time_left/60)} Minute Timer")  #custom name for custom timers
        else:
            TimerWindow(self.root, self.time_left, self.selected_note)  #Pass over the selected note and time

    def remove_timer(self):
        """Remove the selected note from the CSV file and update the Listbox"""
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showerror("No selection", "Please select a timer to remove.")
            return

        #get the index of the selected timer
        selected_index = selected[0]

        #extract the timer to remove
        note_to_remove = self.csv_data[selected_index + 1][0]

        confirm = messagebox.askyesno("Remove Timer", f"Are you sure you want to remove the timer: '{note_to_remove}'?")
        if confirm:
            #remove the selected row from the csv file
            del self.csv_data[selected_index + 1]

            #update the csv file
            with open('timer.csv', mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(self.csv_data)

            #update the Listbox
            self.listbox.delete(selected_index)
            messagebox.showinfo("Removed", f"The note '{note_to_remove}' has been removed.")

    def save_timer(self):
        #Open a window to save a new note to the csv
        save_window = tk.Toplevel(self.root,bg="#F9FFF7")
        save_window.title("Save Timer")

        def save_data():
            note = note_entry.get()
            minutes = minutes_entry.get()

            if not note or not minutes.isdigit() or int(minutes) < 0:
                messagebox.showerror("Invalid input", "Please enter valid note and minutes!")
                return

            #Add the new note and time to the csv file
            minutes = int(minutes)
            self.csv_data.append([note, minutes])

            #update the csv file
            with open('timer.csv', mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(self.csv_data)

            #update Listbox
            self.listbox.insert(tk.END, f" {note} - {minutes} min")
            save_window.destroy()  #Close the save window
            messagebox.showinfo("Saved", f"Note '{note}' saved successfully.")

        tk.Label(save_window, text="Enter note:",font=("Times New Roman",20),width=20,bg="#F9FFF7").pack(padx=10, pady=5)
        note_entry = tk.Entry(save_window, font=(20),relief="sunken",bd=2)
        note_entry.pack(padx=10, pady=5)

        tk.Label(save_window, text="Enter minutes:",font=("Times New Roman",20),width=20,bg="#F9FFF7").pack(padx=10, pady=5)
        minutes_entry = tk.Entry(save_window, font=(20),relief="sunken",bd=2)
        minutes_entry.pack(padx=10, pady=5)

        save_button = tk.Button(save_window, text="Save", font=("Times New Roman",20), command=save_data)
        save_button.pack(padx=5, pady=10)

class TimerWindow:
    def __init__(self, parent_window, time_left, note):
        self.time_left = time_left
        self.note = note  #store the note from the csv file
        self.running = True
        self.time_paused = 0  #store paused time
        self.timer_running = None  #to store the timer callback reference
        
        #create a 'child' window for the countdown timer
        self.counter = tk.Toplevel(parent_window,bg="#FEE9E7",relief="groove",bd=3)
        self.counter.title("Countdown Timer")

        self.frameA = tk.Frame(self.counter, bg="#FEE9E7", padx=20, pady=10)
        self.frameA.grid(row=0, column=0,sticky="ew")
        self.frameB = tk.Frame(self.counter, bg="#FEE9E7", padx=20)
        self.frameB.grid(row=1, column=0)
        self.frameC = tk.Frame(self.counter, bg="#FEE9E7", padx=20, pady=2)
        self.frameC.grid(row=2, column=0)

        #label
        self.timer_label = tk.Label(self.frameA, text="00:00", font=("Times New Roman",30), width=20, bg = "white", relief="groove",bd=2)
        self.timer_label.pack(pady=20)

        #Stop Button
        self.stop_button = tk.Button(self.frameB, text="Stop", font=("Times New Roman",20), command=self.stop_timer, width=10, relief = "raised", bd=4)
        self.stop_button.grid(column=0,row=0)
        #Continue Button
        self.continue_button = tk.Button(self.frameB, text="Continue", font=("Times New Roman",20), command=self.continue_timer, state=tk.DISABLED, width=10, relief = "raised", bd=4)
        self.continue_button.grid(column=1,row=0)
        #End Timer Button
        self.end_button = tk.Button(self.frameC, text="End Timer", font=("Times New Roman",20), command=self.end_timer, width=10, relief = "raised", bd=4)
        self.end_button.pack(pady=5)

        self.start_timer()

    def start_timer(self):
        #Start the countdown timer
        if self.time_left > 0:
            self.running = True
            self.update_timer()

    def update_timer(self):
        #This function will update the timer every second
        if self.running and self.time_left > 0:
            minutes, seconds = divmod(self.time_left, 60) 
            #divmod(a,b) returns minutes = quotient and seconds = remainder
            self.timer_label.config(text=f"{minutes:02}:{seconds:02}")
            #display the time in the format 00:00
            self.time_left -= 1
            self.timer_running = self.counter.after(1000, self.update_timer)
            #.after(delay, callback) calls the function after the delay of 1000 milliseconds i.e. one second

        elif self.time_left == 0:
            self.timer_label.config(text="00:00")
            messagebox.showinfo(f"{self.note} Timer", f"The {self.note} timer has ended!")
            #reset all values and close the timer window
            self.running = False
            self.time_left = 0
            self.time_paused = 0
            self.counter.destroy()

    def stop_timer(self):
        #stop the timer 
        if self.timer_running:
            self.counter.after_cancel(self.timer_running)
            self.running = False
            self.time_paused = self.time_left  #save the time left when stopped
            self.continue_button.config(state=tk.NORMAL)

    def continue_timer(self):
        #continue the timer from the paused time
        if not self.running and self.time_paused > 0:
            self.running = True
            self.time_left = self.time_paused
            self.continue_button.config(state=tk.DISABLED)
            self.update_timer()

    def end_timer(self):
        #end the timer and close the Toplevel window
        respond = messagebox.askyesno("End Timer", "Are you sure you want to end the timer?")
        if respond:
            if self.timer_running:
                self.counter.after_cancel(self.timer_running)
            self.running = False
            self.time_left = 0
            self.time_paused = 0
            self.counter.destroy()  #close the 'child' window

