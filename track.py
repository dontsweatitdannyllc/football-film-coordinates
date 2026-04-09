import argparse, json
import cv2
from ultralytics import YOLO

parser = argparse.ArgumentParser()
parser.add_argument('--input', required=True, help='Path to downsampled video')
parser.add_argument('--model', default='yolov8n.pt', help='YOLOv8 model weights (e.g. yolov8n.pt, yolov8s.pt)')
parser.add_argument('--out', default='tracks_raw.json')
parser.add_argument('--classes', default='0,32', help='Comma-separated class ids to track (0=person, 32=sports ball in COCO)')
args = parser.parse_args()

class_ids = [int(x.strip()) for x in args.classes.split(',') if x.strip()]

model = YOLO(args.model)
cap = cv2.VideoCapture(args.input)
if not cap.isOpened():
    raise SystemExit(f"Could not open video: {args.input}")

frame_id = 0
tracks = {}

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model.track(frame, persist=True, classes=class_ids, verbose=False)
    detections = []

    boxes = results[0].boxes
    if boxes is not None and boxes.id is not None:
        for box, tid in zip(boxes.xyxy, boxes.id):
            x1, y1, x2, y2 = box
            cx = float((x1 + x2) / 2)
            cy = float((y1 + y2) / 2)
            detections.append({
                'player_id': int(tid),
                'cx': cx,
                'cy': cy
            })

    tracks[frame_id] = detections
    frame_id += 1

cap.release()

with open(args.out, 'w') as f:
    json.dump(tracks, f)

print(f"Tracking complete. Wrote {args.out} ({frame_id} frames)")
