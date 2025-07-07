import json
import os
from datetime import datetime

class JSONLogger:
    def __init__(self, output_path):
        self.output_path = output_path

        # Ensure parent folder exists
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

        # Initialize the file with an empty list if it doesn't exist or is empty
        if not os.path.exists(self.output_path) or os.path.getsize(self.output_path) == 0:
            with open(self.output_path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4)

    def log_detection(self, frame_num, bbox, conf, anomaly):
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "frame": frame_num,
            "person": {
                "x": bbox[0],
                "y": bbox[1],
                "w": bbox[2] - bbox[0],
                "h": bbox[3] - bbox[1],
                "conf": round(conf, 2)
            },
            "anomaly_detected": anomaly
        }

        # Append the entry to the existing list
        try:
            with open(self.output_path, "r+", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []

                data.append(entry)
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()  # Remove any leftover content
        except Exception as e:
            print(f"[Logger Error] Failed to write log: {e}")
