import cv2, json, argparse

parser = argparse.ArgumentParser()
parser.add_argument('--frame', default='calibration_frame.jpg', help='Path to image frame used for calibration')
parser.add_argument('--out', default='homography.json')
args = parser.parse_args()

points = []

def click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))

img = cv2.imread(args.frame)
if img is None:
    raise SystemExit(f"Could not read frame image: {args.frame}")

cv2.namedWindow('calibrate', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('calibrate', click)

print('Click 4 anchor points in order (e.g. BL, BR, TR, TL). Press ESC when done.')

while True:
    vis = img.copy()
    for i, (x, y) in enumerate(points):
        cv2.circle(vis, (x, y), 6, (0, 255, 255), -1)
        cv2.putText(vis, str(i+1), (x+8, y-8), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)

    cv2.imshow('calibrate', vis)
    key = cv2.waitKey(20) & 0xFF
    if key == 27:
        break

cv2.destroyAllWindows()

if len(points) != 4:
    raise SystemExit(f"Need exactly 4 points, got {len(points)}")

# Default field rectangle (yards). You can change these to match your anchors.
field = [
    (0.0, 0.0),
    (120.0, 0.0),
    (120.0, 53.3),
    (0.0, 53.3)
]

with open(args.out, 'w') as f:
    json.dump({'pixels': points, 'field': field}, f, indent=2)

print(f"Saved {args.out}")
