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

# detect pre-snap frame using motion analysis
prev_gray = None
motion_scores = []

for i in range(frame_count):
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if prev_gray is None:
        prev_gray = gray
        motion_scores.append(999999)
        continue

    diff = cv2.absdiff(prev_gray, gray)
    score = diff.mean()

    motion_scores.append(score)

    prev_gray = gray

# find frame with lowest motion (pre-snap)
presnap_frame = motion_scores.index(min(motion_scores))

# sample around pre-snap
sample_ids = [
    max(presnap_frame - 2, 0),
    presnap_frame,
    min(presnap_frame + 2, frame_count-1)
]

cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

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
