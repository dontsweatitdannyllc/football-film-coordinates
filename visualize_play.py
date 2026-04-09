import json
import cv2
import numpy as np

# Field dimensions (yards)
FIELD_LENGTH = 120
FIELD_WIDTH = 53.3

# Scale factor for rendering
SCALE = 10

WIDTH = int(FIELD_LENGTH * SCALE)
HEIGHT = int(FIELD_WIDTH * SCALE)

INPUT_JSON = "play_coordinates.json"
OUTPUT_VIDEO = "play_visualization.mp4"
FPS = 10

with open(INPUT_JSON) as f:
    data = json.load(f)

frames = sorted(data.keys(), key=lambda x: int(x.split("_")[1]))

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, FPS, (WIDTH, HEIGHT))

for f in frames:
    img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

    for p in data[f]:
        x = int(p["x"] * SCALE)
        y = int(p["y"] * SCALE)

        # flip y axis so origin is bottom-left
        y = HEIGHT - y

        cv2.circle(img, (x, y), 4, (0, 255, 0), -1)

    cv2.imshow("Play Visualization", img)
    out.write(img)

    if cv2.waitKey(int(1000 / FPS)) == 27:
        break

out.release()
cv2.destroyAllWindows()

print(f"Saved visualization video to {OUTPUT_VIDEO}")
