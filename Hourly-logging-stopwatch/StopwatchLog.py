import time
import tkinter as tk
from tkinter import messagebox
import pandas as pd  # Added for CSV
import os           # Added for CSV

class Stopwatch:
    def __init__(self, label):
        self.start_time = None
        self.elapsed_time = 0
        self.running = False
        self.label = label
        self.last_accomplishment_time = 0  # Tracks last accomplishment prompt time in hours
        self.accomplishment_count = 0  # Track the number of accomplishments
        self.update_timer()

    def start(self):
        if not self.running:
            self.start_time = time.time() - self.elapsed_time
            self.running = True
            self.update_timer()
            print("Stopwatch started")

    def pause(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            self.running = False
            print("Stopwatch paused")

    def reset(self):
        self.start_time = None
        self.elapsed_time = 0
        self.last_accomplishment_time = 0
        self.accomplishment_count = 0
        self.running = False
        self.label.config(text="00:00:00")  # Fix: Instantly update label on reset
        print("Stopwatch reset")

    def get_time(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
        return self.elapsed_time

    def update_timer(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            mins, secs = divmod(self.elapsed_time, 60)
            hours, mins = divmod(mins, 60)
            time_format = '{:02d}:{:02d}:{:02d}'.format(int(hours), int(mins), int(secs))
            self.label.config(text=time_format)
            self.check_accomplishment_prompt()
        self.label.after(1000, self.update_timer)

    def check_accomplishment_prompt(self):
        # Calculate the total elapsed time in hours
        elapsed_hours = self.elapsed_time // 3600
        if elapsed_hours > self.last_accomplishment_time:
            self.last_accomplishment_time = elapsed_hours
            self.accomplishment_count += 1
            accomplishment = self.ask_accomplishment()
            if accomplishment:
                self.record_accomplishment(accomplishment)

    def ask_accomplishment(self):
        dialog = tk.Toplevel(root)
        dialog.title("Accomplishment")
        tk.Label(dialog, text="An hour has passed. Please write what you have accomplished:").pack(pady=10)

        text = tk.Text(dialog, width=40, height=10, wrap=tk.WORD)
        text.pack(pady=10)

        accomplishment = []

        def submit():
            accomplishment.append(text.get("1.0", tk.END).strip())
            dialog.destroy()

        submit_button = tk.Button(dialog, text="Submit", command=submit)
        submit_button.pack(pady=10)

        dialog.transient(root)  # Set to be on top of the main window
        dialog.grab_set()  # Ensure all input goes to the dialog
        # Center the dialog on the screen
        root.update_idletasks()  # Update "requested size" from geometry manager
        dialog_width = dialog.winfo_reqwidth()
        dialog_height = dialog.winfo_reqheight()
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        position_right = int(screen_width/2 - dialog_width/2)
        position_down = int(screen_height/2 - dialog_height/2)
        dialog.geometry(f"{dialog_width}x{dialog_height}+{position_right}+{position_down}")

        root.wait_window(dialog)  # Wait for the dialog to close

        return accomplishment[0] if accomplishment else None

    def record_accomplishment(self, accomplishment):
        # 1. Log to text file (existing logic)
        with open("accomplishments.txt", "a") as file:
            file.write("\n")
            file.write(f"Accomplishment #{self.accomplishment_count}\n")
            file.write(f"Time: {time.strftime('%A, %B %d, %Y - %I:%M %p')}\n")
            file.write("-" * 40 + "\n")
            file.write(accomplishment + "\n")
            file.write("=" * 40 + "\n")

        # 2. Log to CSV
        csv_path = "structured_worklog_by_session.csv"
        now = time.localtime()
        standard_date = time.strftime('%Y-%m-%d', now)
        day_short = time.strftime('%a', now)
        pretty_date = time.strftime('%d %B (%a) %Y', now)
        acc_num = self.accomplishment_count
        acc_time = time.strftime('%I:%M %p', now)
        acc_full_text = f"{acc_time}\n{accomplishment}"

        # Load or initialize CSV
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
        else:
            df = pd.DataFrame()

        # If Accomplishment #1, start new session/row
        if acc_num == 1:
            row = {
                "Standard Date": standard_date,
                "Day": day_short,
                "Date": pretty_date,
                f"Accomplishment 1": acc_full_text
            }
            # Ensure correct columns exist
            columns = ["Standard Date", "Day"] + [f"Accomplishment {i}" for i in range(1, 21)] + ["Date"]
            for col in columns:
                if col not in row:
                    row[col] = ""
            df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        else:
            # Update the most recent session row (last row)
            colname = f"Accomplishment {acc_num}"
            if colname not in df.columns:
                df[colname] = ""
            df.at[df.index[-1], colname] = acc_full_text

        # Save back to CSV
        df.to_csv(csv_path, index=False)

# --- Button Feedback for UX (minimal intrusion) ---
def button_feedback(btn, color="#ffd700", delay=200):
    # #ffd700 is bright gold/yellow; 200ms is longer than before for clarity
    original_color = btn.cget("background")
    btn.config(background=color, activebackground=color)
    btn.after(delay, lambda: btn.config(background=original_color, activebackground=original_color))


# Setup the GUI
root = tk.Tk()
root.title("Stopwatch")

time_label = tk.Label(root, text="00:00:00", font=("Helvetica", 48))
time_label.pack(pady=20)

start_button = tk.Button(root, text="Start", font=("Helvetica", 14))
start_button.pack(side=tk.LEFT, padx=20)

pause_button = tk.Button(root, text="Pause", font=("Helvetica", 14))
pause_button.pack(side=tk.LEFT, padx=20)

reset_button = tk.Button(root, text="Reset", font=("Helvetica", 14))
reset_button.pack(side=tk.LEFT, padx=20)

# --- Updated commands to add button feedback ---
def start_command():
    button_feedback(start_button)
    stopwatch.start()

def pause_command():
    button_feedback(pause_button)
    stopwatch.pause()

def reset_command():
    button_feedback(reset_button)
    stopwatch.reset()

start_button.config(command=start_command)
pause_button.config(command=pause_command)
reset_button.config(command=reset_command)

# Create Stopwatch instance
stopwatch = Stopwatch(time_label)

def on_closing():
    root.destroy()

# Handle the window closing
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the GUI event loop
root.mainloop()
