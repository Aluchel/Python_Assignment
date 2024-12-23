import tkinter as tk
from tkinter import messagebox

class CountdownTimer:
    def __init__(self, root):
        self.root = root 
        #this class is seen as a sort of 'child' window
        #so declaring 'self.root = Tk()' is wrong 
        self.root.title("Countdown Timer")

        self.time_left = 0
        self.running = False
        self.timer_running = False
        self.time_paused = 0  #Transfer the paused time over to this variable
        
        self.frame1=tk.Frame(root)

        #Items on the tkinter window 
        self.notify_label = tk.Label(root, text="The timer counts down time by minutes...",font=(10))
        self.notify_label.grid(row=0, column=0,padx=5)
        self.time_label = tk.Label(root, text="Set Time (in minutes):",font=(10)) 
        self.time_label.grid(row=1, column=0, padx=5, pady=5)

        self.time_entry = tk.Entry(root)
        self.time_entry.grid(row=1, column=1, padx=10, pady=5)
        #Start the timer countdown
        self.start_button = tk.Button(root, text="Start",font=(10), command=self.start_timer)
        self.start_button.grid(row=2, column=0)

        self.stop_button = tk.Button(root, text="Stop",font=(10), command=self.stop_timer)
        self.stop_button.grid(row=2, column=1)

        self.continue_button = tk.Button(root, text="Continue",font=(10), command=self.continue_timer, state=tk.DISABLED)
        self.continue_button.grid(row=2, column=2)

        self.reset_button = tk.Button(root, text="Reset",font=(10), command=self.reset_timer)
        self.reset_button.grid(row=2, column=3)

        self.countdown = tk.Label(root, text="00:00", font=("Times New Roman", 30))
        self.countdown.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    def start_timer(self):
        if not self.running:
            try:
                #Convert the input from user into minutes
                self.time_left = int(self.time_entry.get()) * 60

            except ValueError:
                messagebox.showerror("Invalid input!", "Please enter a valid number for time!")
                #Displays error messagebox when not number

            else:
                self.running = True #When running is true, the time is counting down
                self.continue_button.config(state=tk.DISABLED)  #Disables the continue button 
                self.update_timer()
    
    def update_timer(self): #The function that is constantly updated to countdown the timer
        if self.running and self.time_left > 0: 
            minutes, seconds = divmod(self.time_left, 60)
            self.countdown.config(text=f"{minutes:02}:{seconds:02}")
            self.time_left -= 1
            self.timer_running = self.root.after(1000, self.update_timer)

        elif self.time_left == 0:
            self.countdown.config(text="00:00")
            messagebox.showinfo("Time's up!", "The Timer has ended!!")
            self.running = False
            #No reseting timer here since its all alrd 0

    def stop_timer(self):
        if self.timer_running:
            self.root.after_cancel(self.timer_running)
            self.running = False
            self.time_paused = self.time_left  #Store the remaining time when the timer stopps
            self.continue_button.config(state=tk.NORMAL)  #Enable continue button when timer is stopped

    def continue_timer(self):
        if not self.running and self.time_paused > 0:
            self.running = True
            self.time_left = self.time_paused  #Give back timer to start counting again
            self.continue_button.config(state=tk.DISABLED)  #Disable continue button when timer continues
            self.update_timer()

    def reset_timer(self):
        if self.running:
            self.root.after_cancel(self.timer_running)
            self.running = False
        
        #reset everything
        self.time_left = 0
        self.time_paused = 0
        self.countdown.config(text="00:00")
        self.time_entry.delete(0, tk.END) #Cleans up the entry bar when timer hits 0
        self.continue_button.config(state=tk.DISABLED)  



def open_timer_window():
    #Note on Toplevel() : very useful tool, makes it so we dont have to create a new window entirely
    timer_window = tk.Toplevel() #convert the button press into a command to open the class
    CountdownTimer(timer_window)

def main():
    root = tk.Tk()
    root.title("Main Menu")
    
    lbl = tk.Label(root, text="Welcome to our Program!", font=("Times New Roman", 30))
    lbl.pack()
    
    btn = tk.Button(root, text="Timer", font=("Times New Roman", 20), command=open_timer_window)
    btn.pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    main()
