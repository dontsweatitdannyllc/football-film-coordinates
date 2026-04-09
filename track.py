from ultralytics import YOLO
import cv2, json

model=YOLO('yolov8n.pt')
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--input',required=True)
args=parser.parse_args()
video=args.input
cap=cv2.VideoCapture(video)
frame_id=0
tracks={}

while True:
 ret,frame=cap.read()
 if not ret: break
 results=model.track(frame,persist=True,classes=[0,32])
 detections=[]
 if results[0].boxes.id is not None:
  for box,tid in zip(results[0].boxes.xyxy,results[0].boxes.id):
   x1,y1,x2,y2=box
   cx=float((x1+x2)/2)
   cy=float((y1+y2)/2)
   detections.append({'id':int(tid),'cx':cx,'cy':cy})
 tracks[frame_id]=detections
 frame_id+=1

with open('tracks_raw.json','w') as f:
 json.dump(tracks,f)

print('tracking complete')
