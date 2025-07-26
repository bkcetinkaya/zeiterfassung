import tkinter as tk
from datetime import datetime, timedelta
import time
import os

LOG_FILE = "work_log.txt"

class TimeTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zeiterfassung")

        self.start_time = None
        self.running = False

        self.label_status = tk.Label(root, text="Status: Nicht gestartet", font=("Arial", 14))
        self.label_status.pack(pady=10)

        self.label_timer = tk.Label(root, text="00:00:00", font=("Arial", 24))
        self.label_timer.pack(pady=10)

        self.btn_start = tk.Button(root, text="Start", command=self.start_timer, width=15, bg="green", fg="white", font=("Arial", 12, "bold"))
        self.btn_start.pack(pady=5)

        self.btn_stop = tk.Button(root, text="Stop", command=self.stop_timer, width=15, bg="red", fg="white", font=("Arial", 12, "bold"), state="disabled")
        self.btn_stop.pack(pady=5)

        self.label_total = tk.Label(root, text="Gesamtarbeitszeit: 00:00:00", font=("Arial", 14))
        self.label_total.pack(pady=10)

        self.update_total_time()

    def format_duration(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def parse_duration(self, duration_str):
        h, m, s = map(int, duration_str.split(":"))
        return timedelta(hours=h, minutes=m, seconds=s)

    def calculate_total_time(self):
        total = timedelta()
        if not os.path.exists(LOG_FILE):
            return total

        with open(LOG_FILE, "r") as f:
            for line in f:
                if "Dauer:" in line:
                    try:
                        parts = line.strip().split("Dauer: ")[1]
                        total += self.parse_duration(parts)
                    except:
                        continue
        return total

    def update_total_time(self):
        total_time = self.calculate_total_time()
        total_seconds = int(total_time.total_seconds())
        formatted = self.format_duration(total_seconds)
        self.label_total.config(text=f"Gesamtarbeitszeit: {formatted}")
        self.root.after(60000, self.update_total_time)  # alle 60 Sekunden aktualisieren

    def start_timer(self):
        if not self.running:
            self.start_time = time.time()
            self.running = True
            self.btn_start.config(state="disabled")
            self.btn_stop.config(state="normal")
            self.label_status.config(text="Status: Laufend")
            self.update_timer()

    def stop_timer(self):
        if self.running:
            end_time = time.time()
            duration_seconds = int(end_time - self.start_time)
            formatted_duration = self.format_duration(duration_seconds)

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_line = f"{now} | Dauer: {formatted_duration}\n"

            with open(LOG_FILE, "a") as f:
                f.write(log_line)

            self.running = False
            self.btn_start.config(state="normal")
            self.btn_stop.config(state="disabled")
            self.label_status.config(text=f"Status: Gestoppt - Dauer: {formatted_duration}")
            self.label_timer.config(text="00:00:00")
            self.update_total_time()

    def update_timer(self):
        if self.running:
            elapsed = time.time() - self.start_time
            self.label_timer.config(text=self.format_duration(elapsed))
            self.root.after(1000, self.update_timer)  # jede Sekunde aktualisieren

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeTrackerApp(root)
    root.mainloop()
