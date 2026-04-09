import argparse, json
import numpy as np
import cv2

parser = argparse.ArgumentParser()
parser.add_argument('--tracks', default='tracks_raw.json', help='Input detection file')
parser.add_argument('--homography', default='homography.json')
parser.add_argument('--out', default='projected_tracks.json')
args = parser.parse_args()

tracks = json.load(open(args.tracks))
h = json.load(open(args.homography))

src = np.array(h['pixels'], dtype='float32')
dst = np.array(h['field'], dtype='float32')

if src.shape != (4, 2) or dst.shape != (4, 2):
    raise SystemExit('homography.json must contain exactly 4 pixel points and 4 field points')

H, _ = cv2.findHomography(src, dst)
if H is None:
    raise SystemExit('Could not compute homography (check point ordering / collinearity)')

proj = {}

for f, players in tracks.items():
    out_players = []
    for p in players:
        pt = np.array([[[p['cx'], p['cy']]]], dtype='float32')
        mapped = cv2.perspectiveTransform(pt, H)[0][0]
        out_players.append({
            'player_id': int(p.get('player_id', p.get('id', -1))),
            'x': float(mapped[0]),
            'y': float(mapped[1]),
        })
    proj[f] = out_players

with open(args.out, 'w') as f:
    json.dump(proj, f)

print(f"Projection complete. Wrote {args.out}")
