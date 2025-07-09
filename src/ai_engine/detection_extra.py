import os
import cv2
import grpc
import numpy as np
from datetime import datetime
from shapely.geometry import Polygon, box
from ultralytics import YOLO

from ai_engine.logger import JSONLogger
from ai_engine.zone_checker2 import calculate_overlap
from generated import service_pb2, service_pb2_grpc


class HumanDetection:
    def __init__(self, model_path, log_path, rtsp_url, grpc_address="localhost:50051", camera_id=1):
        self.model = YOLO(model_path)
        self.cap = cv2.VideoCapture(rtsp_url)
        self.logger = JSONLogger(log_path)
        self.frame_count = 1
        self.camera_id = camera_id
        self.anomaly_active = False
        self.anomaly_id_counter = 0


        if not self.cap.isOpened():
            print("Error: Couldn't open the video stream.")
            exit()

        # Setup gRPC
        self.channel = grpc.insecure_channel(grpc_address)
        self.stub = service_pb2_grpc.SurveillanceStub(self.channel)

        # Fetch zone info from backend
        zone_request = service_pb2.ZoneRequest(camera_id=self.camera_id)
        zone_data = self.stub.GetZoneData(zone_request)

        if not zone_data.zones:
            print("No zones received from backend.")
            exit()

        first_zone = zone_data.zones[0]
        self.zone_id = first_zone.zone_id
        self.rules = first_zone.rules

        # Decode the polygon zone coordinates
        zone_coords = first_zone.zone_coord
        if len(zone_coords) < 6 or len(zone_coords) % 2 != 0:
            print("Invalid zone coordinates received.")
            exit()

        self.zone_polygon = [(zone_coords[i], zone_coords[i + 1]) for i in range(0, len(zone_coords), 2)]

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

            # Draw the zone polygon
            cv2.polylines(annotated_frame, [np.array(self.zone_polygon, np.int32)],
                          isClosed=True, color=(0, 0, 255), thickness=2)

            for box in results[0].boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                conf = box.conf[0].item()

                overlap_ratio = calculate_overlap([x1, y1, x2, y2], self.zone_polygon)
                is_anomaly = overlap_ratio > 0.2
                is_near_miss = overlap_ratio > 0.1

                color = (0, 0, 255) if is_anomaly else (0, 255, 0)
                label = f"{'Anomaly' if is_anomaly else 'Near Miss' if is_near_miss else 'Normal'} {conf:.2f}"
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(annotated_frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                # Log locally
                if is_anomaly:
                    self.logger.log_detection(
                        self.frame_count, [x1, y1, x2, y2], conf, is_anomaly
                    )
                
                if is_near_miss:
                    self.logger.log_detection(
                        self.frame_count, [x1, y1, x2, y2], conf, is_near_miss
                    )

                # Send alert if anomaly
                # if is_anomaly:
                #     _, img_encoded = cv2.imencode(".jpg", annotated_frame)
                #     image_bytes = img_encoded.tobytes()

                #     alert = service_pb2.AlertData(
                #         camera_id=self.camera_id,
                #         zone_id=self.zone_id,
                #         alert_type=0,
                #         rules=self.rules,
                #         confidence=int(conf * 100),
                #         timestamp=datetime.now().isoformat(),
                #         image=image_bytes
                #     )
                #     ack = self.stub.SendAlert(alert)
                #     print(f"[gRPC] Alert sent. Success: {ack.success}")

                # if is_anomaly:
                #     if not self.anomaly_active:
                #         # New anomaly starts
                #         self.anomaly_active = True
                #         self.anomaly_id_counter += 1
                #         current_anomaly_id = f"A-{self.anomaly_id_counter:04d}"

                #         # Log
                #         self.logger.log_detection(
                #             self.frame_count, [x1, y1, x2, y2], conf, is_anomaly, anomaly_id=current_anomaly_id
                #         )

                #         # Encode and send snapshot
                #         _, img_encoded = cv2.imencode(".jpg", annotated_frame)
                #         image_bytes = img_encoded.tobytes()

                #         alert = service_pb2.AlertData(
                #             camera_id=self.camera_id,
                #             zone_id=self.zone_id,
                #             alert_type=0,
                #             rules=self.rules,
                #             confidence=int(conf * 100),
                #             timestamp=datetime.now().isoformat(),
                #             image=image_bytes
                #         )
                #         ack = self.stub.SendAlert(alert)
                #         print(f"[gRPC] Alert sent. Success: {ack.success} | ID: {current_anomaly_id}")
                # else:
                #     # Reset anomaly flag when anomaly ends
                #     self.anomaly_active = False
                if is_anomaly:
                    if not self.anomaly_active:
                        # New anomaly starts
                        self.anomaly_active = True
                        self.anomaly_id_counter += 1
                        self.current_anomaly_id = f"A-{self.anomaly_id_counter:04d}"

                        # Send alert only once
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
                        print(f"[gRPC] Alert sent. Success: {ack.success} | ID: {self.current_anomaly_id}")

                    # Log anomaly frame every time
                    self.logger.log_detection(
                        self.frame_count, [x1, y1, x2, y2], conf, is_anomaly, anomaly_id=self.current_anomaly_id
                    )

                else:
                    
                    self.anomaly_active = False
                    self.current_anomaly_id = None


            self.frame_count += 1
            cv2.imshow(window_name, annotated_frame)

            if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    rtsp_url = 0  # Replace with your RTSP URL if needed
    model_path = os.path.abspath("models/yolov8n.pt")
    log_path = os.path.abspath("data-op/bounding_boxes3.json")

    detector = HumanDetection(model_path, log_path, rtsp_url)
    detector.detect_humans()
