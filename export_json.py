import json

tracks=json.load(open('projected_tracks.json'))

out={}
for f,players in tracks.items():
 out[f'frame_{f}']=players

json.dump(out,open('play_coordinates.json','w'),indent=2)

print('exported play_coordinates.json')
