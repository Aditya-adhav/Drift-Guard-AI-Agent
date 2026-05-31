import os
import json

def check_logs():
    log_file = "drift_guard_debug.log"
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            print(f.read())
    else:
        print("Log file not found.")

if __name__ == "__main__":
    check_logs()
