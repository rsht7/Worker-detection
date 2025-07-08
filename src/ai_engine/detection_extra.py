import os
import cv2
import grpc
from ultralytics import YOLO
from datetime import datetime

from .logger import JSONLogger
from .zone_checker import calculate_overlap

# gRPC generated files
from src.generated import service_pb2, service_pb2_grpc

class HumanDetection:
    def __init__(self, model_path, log_path, rtsp_url, grpc_address="localhost:50051", camera_id=1):
        self.model = YOLO(model_path)
        self.cap = cv2.VideoCapture(rtsp_url)
        self.logger = JSONLogger(log_path)
        self.frame_count = 1
        self.camera_id = camera_id

        if not self.cap.isOpened():
            print("Error: Couldn't open the video stream.")
            exit()

        # gRPC channel and stub
        self.channel = grpc.insecure_channel(grpc_address)
        self.stub = service_pb2_grpc.SurveillanceStub(self.channel)

        # Fetch zone data
        zone_request = service_pb2.ZoneRequest(camera_id=self.camera_id)
        zone_data = self.stub.GetZoneData(zone_request)

        if not zone_data.zones:
            print("No zones received from backend.")
            exit()

        self.zone_id = zone_data.zones[0].zone_id
        self.rules = zone_data.zones[0].rules

        # Hardcoded fallback zone until masks are parsed
        self.zone_rect = [0, 0, 300, 600]  # TODO: replace with decoded zone

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

            # Draw zone
            zx1, zy1, zx2, zy2 = self.zone_rect
            cv2.rectangle(annotated_frame, (zx1, zy1), (zx2, zy2), (0, 0, 255), 2)

            for box in results[0].boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                conf = box.conf[0].item()
                overlap_ratio = calculate_overlap([x1, y1, x2, y2], self.zone_rect)
                is_anomaly = overlap_ratio > 0.2

                color = (0, 0, 255) if is_anomaly else (0, 255, 0)
                label = f"{'Anomaly' if is_anomaly else 'Normal'} {conf:.2f}"
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(annotated_frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                # Log locally
                self.logger.log_detection(
                    self.frame_count, [x1, y1, x2, y2], conf, is_anomaly
                )

                if is_anomaly:
                    _, img_encoded = cv2.imencode(".jpg", annotated_frame)
                    image_bytes = img_encoded.tobytes()

                    alert = service_pb2.AlertData(
                        camera_id=self.camera_id,
                        zone_id=self.zone_id,
                        alert_type=0,
                        rules=self.rules,
                        confidence=int(conf * 100),
                        timestamp=datetime.now().isoformat(),
                        image=image_bytes
                    )
                    ack = self.stub.SendAlert(alert)
                    print(f"[gRPC] Alert sent. Success: {ack.success}")

            self.frame_count += 1
            cv2.imshow(window_name, annotated_frame)

            if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

# Optional main function
if __name__ == "__main__":
    rtsp_url = 0  # Use 0 for webcam or your RTSP stream
    model_path = os.path.abspath("models/yolov8n.pt")
    log_path = os.path.abspath("data-op/bounding_boxes2.json")
    detector = HumanDetection(model_path, log_path, rtsp_url)
    detector.detect_humans()
