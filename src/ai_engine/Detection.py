import os
import cv2
from ultralytics import YOLO
from ai_engine.logger import JSONLogger
from ai_engine.zone_checker import calculate_overlap

# Define the zone rectangle (from backend)
ZONE_RECT = [20, 0, 200, 400]  # Example: top-left (x1, y1), bottom-right (x2, y2)

class HumanDetection:
    def __init__(self, model_path, log_path, rtsp_url):
        self.model = YOLO(model_path)
        self.cap = cv2.VideoCapture(rtsp_url)
        self.logger = JSONLogger(log_path)
        self.frame_count = 1

        if not self.cap.isOpened():
            print("Error: Couldn't open the video stream.")
            exit()

    def detect_humans(self):
        window_name = "Human Detection"
        cv2.namedWindow(window_name)

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame.")
                break

            results = self.model.predict(source=frame, classes=[0], conf=0.55, verbose=False)
            annotated_frame = results[0].plot()

            # Draw zone rectangle
            zx1, zy1, zx2, zy2 = ZONE_RECT
            cv2.rectangle(annotated_frame, (zx1, zy1), (zx2, zy2), (0, 0, 255), 2)

            for box in results[0].boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                conf = box.conf[0].item()
                overlap_ratio = calculate_overlap([x1, y1, x2, y2], ZONE_RECT)
                is_anomaly = overlap_ratio > 0.2

                # Annotate with anomaly info
                color = (0, 0, 255) if is_anomaly else (0, 255, 0)
                label = f"{'Anomaly' if is_anomaly else 'Normal'} {conf:.2f}"
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(annotated_frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                # Log the detection
                self.logger.log_detection(
                    self.frame_count, [x1, y1, x2, y2], conf, is_anomaly
                )

            self.frame_count += 1
            cv2.imshow(window_name, annotated_frame)

            if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    rtsp_url = 'rtsp://172.20.10.45:8554/mystream'
      # Replace with RTSP if needed
    # model_path = ".../models/yolov8n.pt"
    model_path = os.path.abspath("models/yolov8n.pt")
    log_path = os.path.abspath("data-op/bounding_boxes2.json")
    detector = HumanDetection(model_path, log_path, rtsp_url)
    detector.detect_humans()
