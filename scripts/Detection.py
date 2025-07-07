import cv2
from ultralytics import YOLO
import time

class HumanDetection:
    def __init__(self, model_path, rtsp_url):
        # Load the YOLOv8 model
        self.model = YOLO(model_path)  # Use 'yolov8n.pt' or your fine-tuned model
        self.rtsp_url = rtsp_url
        
        # Open the RTSP stream
        self.cap = cv2.VideoCapture(rtsp_url)
        if not self.cap.isOpened():
            print("Error: Couldn't open the video stream.")
            exit()
        
        self.frame_count = 0
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)

    def detect_humans(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame.")
                break

            self.frame_count += 1

            # Perform inference (only detect class 0 = person)
            results = self.model.predict(source=frame, classes=[0], conf=0.3, verbose=False)

            annotated_frame = results[0].plot()  # Draw bounding boxes on a copy of the frame

            # Loop through detections
            for box in results[0].boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                conf = box.conf[0].item()

                # Save bounding box coordinates to file
                with open("./data-op/bounding_boxes.txt", "a") as f:
                    f.write(f"Frame {self.frame_count}: Person - x: {int(x1)}, y: {int(y1)}, w: {int(x2 - x1)}, h: {int(y2 - y1)}, conf: {conf:.2f}\n")

            # Show the frame
            cv2.imshow("Human Detection", annotated_frame)

            # Break on 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    rtsp_url = 0  # Replace with your RTSP link or use 0 for laptop cam
    # rtsp://username:password@IP:port
    model_path = "./models/yolov8n.pt"  # Or yolov8s.pt, yolov8n-seg.pt, etc.

    human_detector = HumanDetection(model_path, rtsp_url)
    human_detector.detect_humans()
