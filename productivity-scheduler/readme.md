# Productivity Scheduler – Dual Timer Mac App

A **minimalist productivity scheduler and timer** for MacOS Monterey.  
Plan your day, work through tasks like school periods, and stay accountable with built-in timers and smooth transitions.

---

## 🚩 Features

- **Multiple Tasks:** Input, edit, reorder, or remove tasks before you begin.
- **Priority/Order:** Control the exact sequence of your work.
- **Dual Timers:**  
  - **Global Timer**: Tracks the total elapsed time for your session.
  - **Task Timer**: Counts down each individual task.
- **Automatic Transitions:** After each task, a 3-minute break auto-starts (with sound/popup).
- **Task Statuses:** Easily see what's Upcoming ⏳, In Progress 🔄, and Completed ✅.
- **Progress Bar:** Visual feedback for task completion.
- **Session Summary:** End-of-day stats and optional save to `.txt`.
- **Pause, Skip, Reset, Light/Dark Mode:** Full control, simple design.

---

## ⚡ Quick Start

**Requirements:**  
- MacOS Monterey (12.7.6) or later  
- Python 3.x (Tkinter included by default)

**How to Run:**  
1. Download or clone this repo.
2. In Terminal, navigate to the project folder.
3. Run:
    ```bash
    python3 productivity_scheduler.py
    ```

---

## 📝 Usage

- **1. Add Tasks:**  
  Enter task name, duration (minutes), and order (priority).  
  You can edit or delete tasks before starting.

- **2. Start Day:**  
  Begins your first task. Both timers start.

- **3. While Working:**  
  - See the current task, time left, and session time.
  - After each task, a 3-minute transition break (auto, with sound).
  - Markers indicate which tasks are done, in progress, or coming up.

- **4. Controls:**  
  - **Pause All:** Pauses both timers.
  - **Skip Task:** Moves to the next task after a transition.
  - **Reset Session:** Start over from scratch.
  - **Light/Dark Mode:** Switch to your preferred look.

- **5. End Session:**  
  A summary of your day appears, with option to export as a `.txt` file.

---

## 🛠️ Technical Notes

- **No Internet Required:** Fully offline, local data only.
- **System Sound:** Uses the Mac’s built-in “Glass” sound for alerts.
- **Performance:** Optimized for older Intel MacBooks (2015+), but should run anywhere Python 3.x is supported.
- **Code:** Single file, clean and commented for learning and extension.

---

## 💡 Example Use Cases

- Schedule your day in focused “school periods.”
- Use for deep work blocks, teaching, grading, or AI learning sessions.
- Review your productivity at the end of each session.

---

## 📦 License

MIT License — Free to use, modify, and share.

---

Made with focus by Haider Hayee.  
*Inspired by classic time management principles and real productivity needs!*