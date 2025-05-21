import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import time
import threading
import sys
import os

# --- MacOS SYSTEM SOUND FUNCTION ---
def play_alert_sound():
    """Play a short system alert sound on macOS (no external dependencies)."""
    if sys.platform == "darwin":
        os.system('afplay /System/Library/Sounds/Glass.aiff &')

# --- TASK CLASS ---
class Task:
    """A Task object holds name, duration, order (priority), status, and time elapsed."""
    def __init__(self, name, duration, order):
        self.name = name
        self.duration = duration  # in minutes
        self.order = order
        self.status = "Upcoming"  # can be Upcoming, In progress, or Completed
        self.elapsed = 0         # seconds spent on this task

# --- MAIN APP CLASS ---
class ProductivityApp(tk.Tk):
    def __init__(self):
        super().__init__()
        # ---- Window setup ----
        self.title("Productivity Scheduler")
        self.geometry("650x540")
        self.resizable(False, False)
        self.style = ttk.Style(self)
        self.light_mode = True
        self.set_theme()
        
        # ---- Data & State ----
        self.tasks = []               # List of Task objects
        self.current_task_index = 0   # Which task is currently active
        self.running = False          # Is the timer running?
        self.paused = False           # Is everything paused?
        self.global_seconds = 0       # Total session time in seconds
        self.task_seconds = 0         # Time spent on current task (seconds)
        self.transition = False       # Are we in a transition break?

        self.build_task_entry_screen()  # Start at task entry

    # --- THEME MANAGEMENT (Light/Dark) ---
    def set_theme(self):
        """Sets the overall theme of the app (light or dark)."""
        if self.light_mode:
            self.configure(bg="#F8FAFC")
            self.style.theme_use('clam')
            self.style.configure("Treeview", background="#F8FAFC", fieldbackground="#F8FAFC", foreground="black")
        else:
            self.configure(bg="#22223B")
            self.style.theme_use('clam')
            self.style.configure("Treeview", background="#22223B", fieldbackground="#22223B", foreground="#F8FAFC")

    def toggle_theme(self):
        """Switch between light and dark mode."""
        self.light_mode = not self.light_mode
        self.set_theme()
        self.update()

    # === 1. TASK ENTRY PHASE ===
    def build_task_entry_screen(self):
        """UI for entering, editing, and ordering tasks."""
        # Clear any previous widgets
        for widget in self.winfo_children():
            widget.destroy()
        self.task_frame = ttk.Frame(self)
        self.task_frame.pack(pady=16)

        ttk.Label(self.task_frame, text="Add Your Tasks", font=("Segoe UI", 18, "bold")).pack(pady=6)
        
        # --- Treeview to display tasks ---
        self.tree = ttk.Treeview(self.task_frame, columns=('Name', 'Duration', 'Order'), show='headings', height=8)
        self.tree.heading('Name', text='Task Name')
        self.tree.heading('Duration', text='Duration (min)')
        self.tree.heading('Order', text='Order')
        self.tree.column('Name', width=200)
        self.tree.column('Duration', width=110, anchor='center')
        self.tree.column('Order', width=70, anchor='center')
        self.tree.pack(pady=10)

        # --- Input widgets for adding tasks ---
        entry_frame = ttk.Frame(self.task_frame)
        entry_frame.pack(pady=6)
        ttk.Label(entry_frame, text="Task Name:").grid(row=0, column=0, padx=2)
        self.task_name_entry = ttk.Entry(entry_frame, width=20)
        self.task_name_entry.grid(row=0, column=1, padx=2)

        ttk.Label(entry_frame, text="Duration (min):").grid(row=0, column=2, padx=2)
        self.duration_entry = ttk.Entry(entry_frame, width=6)
        self.duration_entry.grid(row=0, column=3, padx=2)

        ttk.Label(entry_frame, text="Order:").grid(row=0, column=4, padx=2)
        self.order_entry = ttk.Entry(entry_frame, width=4)
        self.order_entry.grid(row=0, column=5, padx=2)

        # --- Add/Edit/Delete task buttons ---
        ttk.Button(entry_frame, text="Add Task", command=self.add_task).grid(row=0, column=6, padx=8)
        ttk.Button(entry_frame, text="Edit Selected", command=self.edit_task).grid(row=0, column=7, padx=8)
        ttk.Button(entry_frame, text="Delete Selected", command=self.delete_task).grid(row=0, column=8, padx=8)
        ttk.Button(self.task_frame, text="Start Day", command=self.start_day).pack(pady=12)

        # --- Theme toggle button (bottom of window) ---
        ttk.Button(self, text="Light/Dark Mode", command=self.toggle_theme).pack(side="bottom", pady=6)

    def add_task(self):
        """Add a task to the list from entry fields."""
        name = self.task_name_entry.get().strip()
        try:
            duration = int(self.duration_entry.get())
            order = int(self.order_entry.get())
            if name and duration > 0:
                task = Task(name, duration, order)
                self.tasks.append(task)
                self.tasks.sort(key=lambda t: t.order)  # Sort by priority/order
                self.refresh_task_tree()
                self.task_name_entry.delete(0, tk.END)
                self.duration_entry.delete(0, tk.END)
                self.order_entry.delete(0, tk.END)
        except:
            messagebox.showerror("Input Error", "Please enter a valid task name, duration, and order.")

    def edit_task(self):
        """Edit the selected task (using pop-up dialogs)."""
        selected = self.tree.selection()
        if not selected:
            return
        idx = self.tree.index(selected)
        task = self.tasks[idx]
        name = simpledialog.askstring("Edit Task", "Edit Task Name:", initialvalue=task.name)
        if name is None: return
        duration = simpledialog.askinteger("Edit Duration", "Edit Duration (min):", initialvalue=task.duration)
        if duration is None: return
        order = simpledialog.askinteger("Edit Order", "Edit Order:", initialvalue=task.order)
        if order is None: return
        task.name = name
        task.duration = duration
        task.order = order
        self.tasks.sort(key=lambda t: t.order)
        self.refresh_task_tree()

    def delete_task(self):
        """Remove the selected task."""
        selected = self.tree.selection()
        if not selected:
            return
        idx = self.tree.index(selected)
        del self.tasks[idx]
        self.refresh_task_tree()

    def refresh_task_tree(self):
        """Update the task table display."""
        self.tree.delete(*self.tree.get_children())
        for task in self.tasks:
            self.tree.insert('', tk.END, values=(task.name, task.duration, task.order))

    def start_day(self):
        """Move to the timer phase after checking tasks are valid."""
        if len(self.tasks) == 0:
            messagebox.showwarning("No Tasks", "Please add at least one task.")
            return
        self.tasks.sort(key=lambda t: t.order)
        for task in self.tasks:
            task.status = "Upcoming"
            task.elapsed = 0
        self.current_task_index = 0
        self.global_seconds = 0
        self.running = True
        self.paused = False
        self.build_timer_screen()
        self.run_timers()

    # === 2. TIMER SCREEN PHASE ===
    def build_timer_screen(self):
        """UI for running timers and showing progress."""
        for widget in self.winfo_children():
            widget.destroy()
        self.timer_frame = ttk.Frame(self)
        self.timer_frame.pack(pady=14)

        # --- Current Task Display ---
        self.current_task_label = ttk.Label(self.timer_frame, text="", font=("Segoe UI", 18, "bold"))
        self.current_task_label.pack(pady=5)

        # --- Timers (Current Task & Global) ---
        timers_frame = ttk.Frame(self.timer_frame)
        timers_frame.pack()
        self.task_timer_label = ttk.Label(timers_frame, text="", font=("Segoe UI", 14))
        self.task_timer_label.grid(row=0, column=0, padx=12)
        self.global_timer_label = ttk.Label(timers_frame, text="", font=("Segoe UI", 14))
        self.global_timer_label.grid(row=0, column=1, padx=12)

        # --- Progress Bar ---
        self.progress = ttk.Progressbar(self.timer_frame, length=350, mode="determinate")
        self.progress.pack(pady=8)

        # --- Task Listbox (status markers) ---
        self.task_listbox = tk.Listbox(self.timer_frame, width=54, height=7, font=("Segoe UI", 12))
        self.task_listbox.pack(pady=6)

        # --- Status/Message Label ---
        self.message_label = ttk.Label(self.timer_frame, text="", font=("Segoe UI", 12, "italic"))
        self.message_label.pack(pady=4)

        # --- Control Buttons (Pause/Skip/Reset/Theme) ---
        ctrl_frame = ttk.Frame(self.timer_frame)
        ctrl_frame.pack(pady=6)
        ttk.Button(ctrl_frame, text="Pause All", command=self.pause_all).grid(row=0, column=0, padx=7)
        ttk.Button(ctrl_frame, text="Skip Task", command=self.skip_task).grid(row=0, column=1, padx=7)
        ttk.Button(ctrl_frame, text="Reset Session", command=self.reset_session).grid(row=0, column=2, padx=7)
        ttk.Button(ctrl_frame, text="Light/Dark Mode", command=self.toggle_theme).grid(row=0, column=3, padx=7)

    def update_timer_screen(self):
        """Refreshes the timer and task status on the timer screen."""
        if self.current_task_index < len(self.tasks):
            current_task = self.tasks[self.current_task_index]
            # Display current task name and timers
            self.current_task_label.config(text=f"Now: {current_task.name}")
            self.task_timer_label.config(
                text=f"Task Time Left: {self.format_time(current_task.duration * 60 - self.task_seconds)}"
            )
            self.global_timer_label.config(
                text=f"Total Time: {self.format_time(self.global_seconds)}"
            )
            self.progress["maximum"] = current_task.duration * 60
            self.progress["value"] = self.task_seconds

            # --- Task Status Display in Listbox ---
            self.task_listbox.delete(0, tk.END)
            for idx, task in enumerate(self.tasks):
                marker = "✅" if task.status == "Completed" else "🔄" if idx == self.current_task_index else "⏳"
                self.task_listbox.insert(tk.END, f"{marker} {task.name} ({task.duration} min)")
        else:
            # All tasks finished
            self.current_task_label.config(text="All tasks finished.")

    def run_timers(self):
        """Main timer loop: updates every second using after()."""
        if not self.running:
            return
        if not self.paused:
            self.global_seconds += 1  # Always increment global session time
            if self.current_task_index < len(self.tasks):
                if not self.transition:
                    # Main task timer running
                    self.task_seconds += 1
                    self.tasks[self.current_task_index].elapsed += 1
                    # Task complete: go to transition
                    if self.task_seconds >= self.tasks[self.current_task_index].duration * 60:
                        self.tasks[self.current_task_index].status = "Completed"
                        play_alert_sound()
                        self.transition = True
                        self.transition_seconds = 0
                        self.message_label.config(text="Transition: Next task starts in 3 minutes.")
                    else:
                        self.message_label.config(text="")
                else:
                    # In transition/break
                    self.transition_seconds += 1
                    self.message_label.config(text="Transition: Next task starts in {} min {:02d} sec.".format(
                        2 - self.transition_seconds // 60, 59 - self.transition_seconds % 60))
                    if self.transition_seconds >= 180:
                        # End of transition, move to next task
                        self.transition = False
                        self.task_seconds = 0
                        self.current_task_index += 1
                        if self.current_task_index < len(self.tasks):
                            self.tasks[self.current_task_index].status = "In progress"
                        play_alert_sound()
            self.update_timer_screen()
        self.after(1000, self.run_timers)  # Loop every second

        # If all tasks finished, show summary once transition is over
        if self.current_task_index >= len(self.tasks) and not self.transition:
            self.running = False
            self.show_summary()

    def format_time(self, seconds):
        """Helper to convert seconds to mm:ss string."""
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins:02d}:{secs:02d}"

    # === CONTROL BUTTONS ===
    def pause_all(self):
        """Pause or resume all timers and UI updates."""
        self.paused = not self.paused
        if self.paused:
            self.message_label.config(text="Paused. Press again to resume.")
        else:
            self.message_label.config(text="Resumed.")

    def skip_task(self):
        """Mark current task complete and immediately enter transition."""
        if self.transition:
            return
        self.tasks[self.current_task_index].status = "Completed"
        self.task_seconds = 0
        self.transition = True
        self.transition_seconds = 0
        play_alert_sound()
        self.message_label.config(text="Transition: Task skipped. Next task starts in 3 minutes.")

    def reset_session(self):
        """Reset everything back to task entry (user confirmation required)."""
        if messagebox.askyesno("Reset", "Are you sure you want to reset the session?"):
            self.running = False
            self.transition = False
            self.build_task_entry_screen()

    # === 3. SESSION SUMMARY ===
    def show_summary(self):
        """Display end-of-session summary and save option."""
        for widget in self.winfo_children():
            widget.destroy()
        sum_frame = ttk.Frame(self)
        sum_frame.pack(pady=32)
        ttk.Label(sum_frame, text="Session Complete!", font=("Segoe UI", 20, "bold")).pack(pady=8)
        ttk.Label(sum_frame, text=f"Total Session Time: {self.format_time(self.global_seconds)}",
                  font=("Segoe UI", 14)).pack(pady=4)
        # --- Display all task details in a text widget ---
        summary_box = tk.Text(sum_frame, height=10, width=60, font=("Segoe UI", 12))
        summary_box.pack(pady=10)
        summary_text = ""
        for task in self.tasks:
            mins, secs = divmod(task.elapsed, 60)
            summary_text += f"{task.name}: {mins} min {secs} sec ({'Completed' if task.status == 'Completed' else 'Skipped'})\n"
        summary_box.insert(tk.END, summary_text)
        summary_box.config(state='disabled')
        ttk.Button(sum_frame, text="Save Summary (.txt)", command=lambda: self.save_summary(summary_text)).pack(pady=6)
        ttk.Button(sum_frame, text="Back to Task Entry", command=self.build_task_entry_screen).pack(pady=6)
        ttk.Label(sum_frame, text="“Great work! Discipline is the bridge between goals and accomplishment.”",
                  font=("Segoe UI", 11, "italic")).pack(pady=14)

    def save_summary(self, text):
        """Export the session summary to a .txt file (user chooses location)."""
        file = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text files", "*.txt")])
        if file:
            with open(file, "w") as f:
                f.write("Productivity Session Summary\n")
                f.write(f"Total Time: {self.format_time(self.global_seconds)}\n\n")
                f.write(text)
            messagebox.showinfo("Saved", "Session summary saved.")

# --- MAIN APP RUN ---
if __name__ == "__main__":
    app = ProductivityApp()
    app.mainloop()
