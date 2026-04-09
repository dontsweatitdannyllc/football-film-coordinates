import cv2,json,numpy as np

tracks=json.load(open('tracks_raw.json'))
h=json.load(open('homography.json'))

src=np.array(h['pixels'],dtype='float32')
dst=np.array(h['field'],dtype='float32')

H,_=cv2.findHomography(src,dst)

proj={}

for f,players in tracks.items():
 out=[]
 for p in players:
  pt=np.array([[p['cx'],p['cy']]],dtype='float32')
  pt=np.array([pt])
  mapped=cv2.perspectiveTransform(pt,H)[0][0]
  out.append({'player_id':p['id'],'x':float(mapped[0]),'y':float(mapped[1])})
 proj[f]=out

json.dump(proj,open('projected_tracks.json','w'))
print('projection complete')
