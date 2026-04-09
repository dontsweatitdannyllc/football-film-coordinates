import argparse, subprocess, os

parser = argparse.ArgumentParser()
parser.add_argument('--video', required=True, help='Path to local MP4 file (720p)')
parser.add_argument('--fps', type=int, default=10)
args = parser.parse_args()

video = args.video
fps = args.fps

base = os.path.splitext(os.path.basename(video))[0]

sampled = f"{base}_{fps}fps.mp4"

print("[1/4] Downsampling FPS...")
subprocess.run(['ffmpeg','-y','-i',video,'-filter:v',f'fps={fps}',sampled])

print("[2/4] Running tracking...")
subprocess.run(['python','track.py'])

print("[3/4] Calibration step (click 4 field points)...")
print("Make sure calibration_frame.jpg exists before running calibrate.")
subprocess.run(['python','calibrate.py'])

print("[4/4] Projecting coordinates + exporting JSON...")
subprocess.run(['python','project.py'])
subprocess.run(['python','export_json.py'])

print("Pipeline complete.")
