import time
import tkinter as tk
from tkinter import messagebox

# Define a class for the stopwatch functionality
class Stopwatch:
    def __init__(self, label):
        # Initialize variables to track start time, elapsed time, and whether the stopwatch is running
        self.start_time = None
        self.elapsed_time = 0
        self.running = False
        self.label = label  # The label on the GUI where time will be displayed
        self.last_accomplishment_time = 0  # Tracks last time the accomplishment prompt was shown (in hours)
        self.accomplishment_count = 0  # Keeps track of how many accomplishments have been logged
        self.update_timer()  # Start updating the timer display immediately

    # Method to start the stopwatch
    def start(self):
        if not self.running:  # Only start if it's not already running
            # Calculate start time by subtracting any previously elapsed time (if resumed after a pause)
            self.start_time = time.time() - self.elapsed_time
            self.running = True
            self.update_timer()  # Continuously update the timer once started
            print("Stopwatch started")

    # Method to pause the stopwatch
    def pause(self):
        if self.running:  # Only pause if it's currently running
            # Calculate elapsed time up to the moment it was paused
            self.elapsed_time = time.time() - self.start_time
            self.running = False  # Stop the timer
            print("Stopwatch paused")

    # Method to reset the stopwatch
    def reset(self):
        # Reset all time-related variables
        self.start_time = None
        self.elapsed_time = 0
        self.last_accomplishment_time = 0
        self.accomplishment_count = 0
        self.running = False  # Ensure the stopwatch is stopped
        self.update_timer()  # Update the GUI with the reset time (00:00:00)
        print("Stopwatch reset")

    # Get the current elapsed time
    def get_time(self):
        if self.running:  # If running, update the elapsed time
            self.elapsed_time = time.time() - self.start_time
        return self.elapsed_time

    # Continuously update the time display every second
    def update_timer(self):
        if self.running:  # Only update the time if the stopwatch is running
            self.elapsed_time = time.time() - self.start_time
            # Convert elapsed time into hours, minutes, and seconds
            mins, secs = divmod(self.elapsed_time, 60)
            hours, mins = divmod(mins, 60)
            # Format time as HH:MM:SS
            time_format = '{:02d}:{:02d}:{:02d}'.format(int(hours), int(mins), int(secs))
            self.label.config(text=time_format)  # Update the label with the current time
            self.check_accomplishment_prompt()  # Check if an hour has passed to prompt for an accomplishment
        # Call update_timer() again after 1 second (1000 ms)
        self.label.after(1000, self.update_timer)

    # Check if an hour has passed since the last accomplishment prompt
    def check_accomplishment_prompt(self):
        # Calculate the total elapsed time in hours
        elapsed_hours = self.elapsed_time // 3600
        # If more than an hour has passed since the last prompt
        if elapsed_hours > self.last_accomplishment_time:
            self.last_accomplishment_time = elapsed_hours  # Update the last prompt time
            self.accomplishment_count += 1  # Increase the accomplishment count
            # Ask the user for their accomplishment
            accomplishment = self.ask_accomplishment()
            if accomplishment:
                # Record the accomplishment if provided
                self.record_accomplishment(accomplishment)

    # Ask the user to input their accomplishment via a dialog box
    def ask_accomplishment(self):
        dialog = tk.Toplevel(root)  # Create a new top-level dialog window
        dialog.title("Accomplishment")  # Title for the dialog
        tk.Label(dialog, text="An hour has passed. Please write what you have accomplished:").pack(pady=10)

        # Create a text input box for the user to enter their accomplishment
        text = tk.Text(dialog, width=40, height=10, wrap=tk.WORD)
        text.pack(pady=10)

        # List to store the user's accomplishment
        accomplishment = []

        # Function to handle when the submit button is clicked
        def submit():
            # Get the entered text, strip any extra spaces/newlines, and store it in accomplishment
            accomplishment.append(text.get("1.0", tk.END).strip())
            dialog.destroy()  # Close the dialog

        # Create a submit button that triggers the submit function
        submit_button = tk.Button(dialog, text="Submit", command=submit)
        submit_button.pack(pady=10)

        # Make sure the dialog is in focus and on top of the main window
        dialog.transient(root)
        dialog.grab_set()  # Lock input to the dialog

        # Center the dialog on the screen
        root.update_idletasks()  # Update the window size before positioning
        dialog_width = dialog.winfo_reqwidth()
        dialog_height = dialog.winfo_reqheight()
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        position_right = int(screen_width/2 - dialog_width/2)
        position_down = int(screen_height/2 - dialog_height/2)
        dialog.geometry(f"{dialog_width}x{dialog_height}+{position_right}+{position_down}")

        # Wait for the dialog to close before proceeding
        root.wait_window(dialog)

        # Return the entered accomplishment or None if nothing was entered
        return accomplishment[0] if accomplishment else None

    # Record the accomplishment in a text file
    def record_accomplishment(self, accomplishment):
        # Open the text file in append mode and write the accomplishment
        with open("accomplishments.txt", "a") as file:
            file.write("\n")
            file.write(f"Accomplishment #{self.accomplishment_count}\n")
            file.write(f"Time: {time.strftime('%A, %B %d, %Y - %I:%M %p')}\n")  # Timestamp of when it was recorded
            file.write("-" * 40 + "\n")
            file.write(accomplishment + "\n")
            file.write("=" * 40 + "\n")

# Functions to start, pause, and reset the stopwatch when buttons are clicked
def start_stopwatch():
    stopwatch.start()

def pause_stopwatch():
    stopwatch.pause()

def reset_stopwatch():
    stopwatch.reset()

# Handle the closing of the main window
def on_closing():
    root.destroy()  # Close the application

# Setup the main GUI window
root = tk.Tk()
root.title("Stopwatch")

# Create the time display label
time_label = tk.Label(root, text="00:00:00", font=("Helvetica", 48))
time_label.pack(pady=20)

# Create the control buttons (Start, Pause, Reset)
start_button = tk.Button(root, text="Start", command=start_stopwatch, font=("Helvetica", 14))
start_button.pack(side=tk.LEFT, padx=20)

pause_button = tk.Button(root, text="Pause", command=pause_stopwatch, font=("Helvetica", 14))
pause_button.pack(side=tk.LEFT, padx=20)

reset_button = tk.Button(root, text="Reset", command=reset_stopwatch, font=("Helvetica", 14))
reset_button.pack(side=tk.LEFT, padx=20)

# Create a Stopwatch instance and associate it with the time display label
stopwatch = Stopwatch(time_label)

# Handle window close event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the main GUI loop
root.mainloop()
