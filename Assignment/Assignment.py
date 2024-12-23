import tkinter as tk
from tkinter import messagebox
from Chun_Hei import *

def open_timer_window():
    #Open a 'child' window
    timer_window = tk.Toplevel()
    CountdownTimer(timer_window)

def main():
    root = tk.Tk()
    root.title("Main Menu")
    
    lbl = tk.Label(root, text="Welcome to our Program!", font=("Times New Roman", 30))
    lbl.grid(row=0, column=0, pady=20)
    
    btn = tk.Button(root, text="Timer", font=("Times New Roman", 20), command=open_timer_window)
    btn.grid(row=1, column=0, pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    main()
