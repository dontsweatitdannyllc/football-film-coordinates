import argparse, subprocess, os

parser = argparse.ArgumentParser()
parser.add_argument('--video', required=True, help='Path to local MP4 file (720p)')
parser.add_argument('--fps', type=int, default=10)
args = parser.parse_args()

video = args.video
fps = args.fps

base = os.path.splitext(os.path.basename(video))[0]

sampled = f"{base}_{fps}fps.mp4"

print("[1/5] Downsampling FPS and normalizing video...")
subprocess.run(['ffmpeg','-y','-i',video,'-vf',f'fps={fps},format=yuv420p',sampled])

print("[2/5] Extracting calibration frame...")
subprocess.run(['ffmpeg','-y','-i',sampled,'-vframes','1','calibration_frame.jpg'])

print("[3/5] Running tracking...")
subprocess.run(['python','track.py','--input',sampled])

print("[4/5] Calibration step (click 4 field points)...")
subprocess.run(['python','calibrate.py'])

print("[5/5] Projecting coordinates + exporting JSON...")
subprocess.run(['python','project.py'])
subprocess.run(['python','export_json.py'])

print("Pipeline complete. Output: play_coordinates.json")
