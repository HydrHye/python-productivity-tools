# Hourly Logging Stopwatch

The **Hourly Logging Stopwatch** is a productivity-enhancing tool designed to help users track their time and accomplishments throughout the day.  
It is built with a simple GUI using Python's `tkinter` library and now offers robust accomplishment tracking with both text and structured CSV logging for easy review and analysis.

---

## Features

- **Start, Pause, and Reset Functions:** The stopwatch can be easily started, paused, and reset with the click of a button.
- **Hourly Log Prompts:** Every hour, a pop-up dialog prompts users to log their accomplishments, helping to reflect on what has been achieved during the time period.
- **Accomplishment Logging:** 
  - All accomplishments are saved in a text file (`accomplishments.txt`), making it easy to track daily productivity in a human-readable format.
  - **NEW:** All accomplishments are also saved to a structured CSV file (`structured_worklog_by_session.csv`), where each work session is grouped into a single row—ideal for use in Excel, Google Sheets, or for analytics.
- **Session-Based Grouping:** The CSV log groups all accomplishments from the same session (starting with Accomplishment #1) under the date of the first accomplishment, even if the session continues past midnight.
- **Enhanced User Experience:** 
  - The timer instantly resets to `00:00:00` when Reset is pressed, for immediate visual feedback.
  - The Start, Pause, and Reset buttons now briefly highlight in a vivid color when pressed, making the interface more responsive and engaging.
- **Simple GUI:** The interface is user-friendly, designed with simplicity in mind to reduce distractions.

---

## How It Works

1. **Start the Stopwatch:** Begin timing by pressing the "Start" button.
2. **Pause or Reset:** Pause or reset the stopwatch at any time.
3. **Hourly Prompts:** After every hour of active timing, a pop-up dialog will ask what you've accomplished during the past hour.
4. **Logging:**
   - All accomplishments are saved in `accomplishments.txt` for a narrative log.
   - **NEW:** All sessions and accomplishments are also saved in `structured_worklog_by_session.csv` for clean, session-based review and analysis.

---

## Requirements

- **Python 3.x**
- **Tkinter** (comes pre-installed with Python on most systems)
- **Pandas** (for CSV logging)
  - Install with:  
    ```bash
    pip install pandas
    ```

---

## How to Run

1. Clone this repository:
    ```bash
    git clone https://github.com/your-username/python-productivity-tools.git
    ```
2. Navigate to the `Hourly-logging-stopwatch` directory:
    ```bash
    cd python-productivity-tools/Hourly-logging-stopwatch
    ```
3. Run the application:
    ```bash
    python3 StopwatchLog.py
    ```

---

## Change Log

- **11 July 2025:**  
  - Added structured CSV logging (`structured_worklog_by_session.csv`) for session-based review.
  - Improved user experience: timer instantly resets, and buttons provide pronounced visual feedback when pressed.

---

## License

MIT License (or your preferred license)

