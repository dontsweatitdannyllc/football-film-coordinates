import cv2,json
points=[]

def click(event,x,y,flags,param):
 if event==cv2.EVENT_LBUTTONDOWN:
  points.append((x,y))

img=cv2.imread('calibration_frame.jpg')
cv2.namedWindow('calibrate')
cv2.setMouseCallback('calibrate',click)

while True:
 cv2.imshow('calibrate',img)
 if cv2.waitKey(1)&0xFF==27: break

print('pixel points:',points)

field=[
(0,0),
(120,0),
(120,53.3),
(0,53.3)
]

json.dump({'pixels':points,'field':field},open('homography.json','w'))
