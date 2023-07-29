import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time
import os
import threading
import winsound

current_dir = os.path.dirname(os.path.abspath(__file__))
sound_file = os.path.join(current_dir, "alarm_sound.wav")

def set_alarm():
    print("Setting alarm...")
    alarm_time = entry.get()
    try:
        time.strptime(alarm_time, "%H:%M")
    except ValueError:
        messagebox.showerror("Error", "Invalid time format. Please use HH:MM.")
        return

    # Update the label to show "Alarm set"
    status_label.config(text="Alarm set")

    def check_alarm():
        print("Checking alarm...")
        current_time = time.strftime("%H:%M")
        if current_time == alarm_time:
            play_alarm_sound()
        else:
            root.after(1000, check_alarm)
    # Start checking the alarm time after the initial delay of 1 second
    root.after(1000, check_alarm)

def play_alarm_sound():
    try:
        print("Playing alarm sound...")
        winsound.PlaySound(sound_file, winsound.SND_FILENAME | winsound.SND_ASYNC)
    except Exception as e:
        print("Error playing sound:", e)

def stop_alarm():
    try:
        print("Stopping alarm sound...")
        winsound.PlaySound(None, winsound.SND_PURGE)
        # Update the label to show "Alarm stopped"
        status_label.config(text="Alarm stopped")
    except Exception as e:
        print("Error stopping sound:", e)


def update_time():
    current_time = time.strftime(f"%H:%M ({'AM' if time_format.get() == 12 else '24-Hour Format'})")
    time_label.config(text=current_time)
    root.after(1000, update_time)

root = tk.Tk()
root.title("Alarm Clock")
root.geometry("300x200")

style = ttk.Style()
style.configure("SetAlarm.TButton", background="green", foreground="white", font=("Arial", 12, "bold"))

time_label = ttk.Label(root, font=("Arial", 24))
time_label.pack(pady=20)

time_format = tk.IntVar(value=24)
update_time()

entry = ttk.Entry(root, font=("Arial", 14))
entry.pack()

set_button = ttk.Button(root, text="Set Alarm", command=set_alarm, style="SetAlarm.TButton")
set_button.pack(pady=10)

stop_button = ttk.Button(root, text="Stop Alarm", command=stop_alarm)
stop_button.pack(pady=5)

status_label = ttk.Label(root, text="", font=("Arial", 14))
status_label.pack()

def snooze():
    print("Snooze...")
    stop_alarm()
    root.after(300000, set_alarm)  # Snooze for 5 minutes (300,000 ms)
snooze_button = ttk.Button(root, text="Snooze", command=snooze)
snooze_button.pack(pady=5)

root.mainloop()
