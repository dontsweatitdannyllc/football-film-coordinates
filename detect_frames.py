import argparse
import json
import cv2
from ultralytics import YOLO

parser = argparse.ArgumentParser()
parser.add_argument('--input', required=True)
parser.add_argument('--out', default='tracks_raw.json')
args = parser.parse_args()

video = args.input
cap = cv2.VideoCapture(video)
if not cap.isOpened():
    raise SystemExit(f"Could not open video: {video}")

frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

sample_ids = [0, frame_count//2, int(frame_count*0.75)]

model = YOLO('yolov8s.pt')

results_json = {}

for idx,i in enumerate(sample_ids):

    cap.set(cv2.CAP_PROP_POS_FRAMES, i)
    ret, frame = cap.read()
    if not ret:
        continue

    # first pass
    res = model(frame, conf=0.15, iou=0.5, classes=[0])[0]

    boxes = []

    if res.boxes is not None:
        for b,c in zip(res.boxes.xyxy, res.boxes.conf):
            x1,y1,x2,y2 = b
            cx = float((x1+x2)/2)
            cy = float((y1+y2)/2)
            boxes.append((float(c), cx, cy))

    # fallback pass if not enough
    if len(boxes) < 22:
        res = model(frame, conf=0.05, iou=0.5, classes=[0])[0]
        boxes = []
        if res.boxes is not None:
            for b,c in zip(res.boxes.xyxy, res.boxes.conf):
                x1,y1,x2,y2 = b
                cx = float((x1+x2)/2)
                cy = float((y1+y2)/2)
                boxes.append((float(c), cx, cy))

    boxes.sort(reverse=True, key=lambda x: x[0])

    boxes = boxes[:22]

    frame_players = []

    for pid,(conf,cx,cy) in enumerate(boxes):
        frame_players.append({
            "player_id": pid,
            "cx": cx,
            "cy": cy
        })

    results_json[idx] = frame_players

cap.release()

with open(args.out,'w') as f:
    json.dump(results_json,f)

print(f"Saved detections to {args.out}")
