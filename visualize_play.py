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

frame_index = 0

while 0 <= frame_index < len(frames):

    f = frames[frame_index]

    img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

    for p in data[f]:

        pid = p.get("player_id",0)

        x = int(p["x"] * SCALE)
        y = int(p["y"] * SCALE)

        y = HEIGHT - y

        cv2.circle(img, (x, y), 5, (0, 255, 0), -1)

        cv2.putText(
            img,
            str(pid),
            (x+6, y-6),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (0,255,0),
            1
        )

    cv2.imshow("Play Visualization", img)

    key = cv2.waitKey(0)

    if key == ord('q'):
        break

    elif key == ord('d'):
        frame_index += 1

    elif key == ord('a'):
        frame_index -= 1

    else:
        frame_index += 1

    out.write(img)

out.release()
cv2.destroyAllWindows()

print(f"Saved visualization video to {OUTPUT_VIDEO}")
