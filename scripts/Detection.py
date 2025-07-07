import cv2
from ultralytics import YOLO
from datetime import datetime
import json
import os

class HumanDetection:
    def __init__(self, model_path, rtsp_url, output_file="./data-op/bounding_boxes.json"):
        self.model = YOLO(model_path)
        self.rtsp_url = rtsp_url
        self.cap = cv2.VideoCapture(rtsp_url)
        self.output_file = output_file

        if not self.cap.isOpened():
            print("Error: Couldn't open the video stream.")
            exit()

        # ✅ Always start frame count from 1 on each run
        self.frame_count = 1

        # ✅ If JSON file doesn't exist, create it as an empty array
        if not os.path.exists(self.output_file):
            with open(self.output_file, "w") as f:
                json.dump([], f)

    def append_to_json(self, detection):
        with open(self.output_file, "r+") as f:
            data = json.load(f)
            data.append(detection)
            f.seek(0)
            json.dump(data, f, indent=4)

    def detect_humans(self):
        window_name = "Human Detection"
        cv2.namedWindow(window_name)

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame.")
                break

            results = self.model.predict(source=frame, classes=[0], conf=0.3, verbose=False)
            annotated_frame = results[0].plot()

            for box in results[0].boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                conf = box.conf[0].item()

                detection_entry = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "frame": self.frame_count,
                    "person": {
                        "x": int(x1),
                        "y": int(y1),
                        "w": int(x2 - x1),
                        "h": int(y2 - y1),
                        "conf": round(conf, 2)
                    }
                }

                self.append_to_json(detection_entry)

            self.frame_count += 1
            cv2.imshow(window_name, annotated_frame)

            if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    rtsp_url = 0  # Or your RTSP link
    model_path = "./models/yolov8n.pt"

    human_detector = HumanDetection(model_path, rtsp_url)
    human_detector.detect_humans()
