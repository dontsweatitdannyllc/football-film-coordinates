# Football Film → Field Coordinates Pipeline

Turn football game film into structured player coordinates that an AI or analytics system can analyze.

This project converts a broadcast video of a play into **player tracking data in field coordinates (yards)**.

The result is a JSON dataset describing where each player is on the field for every frame of the play.

This is the core primitive needed for:

• automated play diagrams  
• route analysis  
• formation detection  
• coverage classification  
• AI scouting assistants  

---

# Pipeline Overview

Input

MP4 football film (720p recommended)

Output

JSON containing tracked players and their field coordinates.

Example:

{
  "frame_10": [
    {"player_id": 1, "x": 20.1, "y": 25.4},
    {"player_id": 7, "x": 22.7, "y": 24.2}
  ]
}

---

# Architecture

Step 1 — Frame Rate Reduction

Reduce video from ~30–60 FPS to ~10 FPS to reduce compute cost.

Tool:

ffmpeg

Script:

sample_frames.py

---

Step 2 — Player Detection + Tracking

Detect players and assign persistent IDs across frames.

Tools:

YOLOv8
ByteTrack

Script:

track.py

Output:

tracks_raw.json

---

Step 3 — Field Calibration (Homography)

Map camera pixels to real field coordinates.

User clicks **4 anchor points** on the field.

Example anchors:

• sideline / yardline intersections  
• hash marks  
• yardline corners

Tool:

OpenCV homography

Script:

calibrate.py

Output:

homography.json

---

Step 4 — Coordinate Projection

Convert each player's pixel centroid into field coordinates.

Tool:

OpenCV perspective transform

Script:

project.py

Output:

projected_tracks.json

---

Step 5 — JSON Export

Convert tracking output into a clean format for AI systems.

Script:

export_json.py

Output:

play_coordinates.json

---

# Installation

Install dependencies:

pip install -r requirements.txt

Requirements include:

• ultralytics  
• opencv-python  
• numpy  
• ffmpeg  

---

# Running the Pipeline

Process a video:

python run_pipeline.py --video play.mp4 --fps 10

Pipeline steps:

1. Downsample video FPS
2. Run YOLO tracking
3. Calibrate field
4. Project coordinates
5. Export JSON

Final output:

play_coordinates.json

---

# Visualizing the Play

You can render the JSON output as a **top‑down animation of the play** using OpenCV.

Run:

python visualize_play.py

This will:

• read `play_coordinates.json`
• render players as dots on a 120 x 53.3 yard field
• play the animation frame‑by‑frame
• export a video file `play_visualization.mp4`

Example output:

A top‑down animation similar to **NFL Next Gen Stats tracking dots**.

This is useful for:

• validating tracking accuracy
• debugging homography calibration
• visualizing player movement

---

# Directory Structure

film_pipeline/

run_pipeline.py
sample_frames.py
track.py
calibrate.py
project.py
export_json.py
requirements.txt
README.md

---

# Example Use Cases

• Generate **All‑22 style play diagrams**  
• Identify offensive formations  
• Classify defensive coverage  
• Measure receiver separation  
• Analyze route trees  
• Build AI scouting assistants

---

# Roadmap

Planned improvements:

• Automatic yard line detection
• Offense / defense classification
• Jersey color clustering
• Route visualization overlays
• Automatic play diagram generation
• Formation recognition
• Coverage classification

---

# Why This Exists

Coaches and scouts still manually review film.

This project turns game film into **structured spatial data** so machines can analyze football the same way analytics transformed baseball and basketball.

The long-term vision is a **fully automated digital scouting assistant**.
