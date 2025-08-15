# Video Analytics Pipeline

This project implements a **multiprocess video analytics pipeline** with three main components:

1. **Streamer** – Extracts frames from a video file and sends them to the detector.
2. **Detector** – Detects motion between consecutive frames and outputs bounding boxes.
3. **Displayer** – Draws detections and timestamps on frames, displays the video, and saves results.

Additionally, the project includes a **watchdog module** that monitors a folder for new video files and automatically starts the pipeline when a new video is detected.

---

## Features

- Real-time video streaming and processing.
- Motion detection between consecutive frames.
- Display of rectangles around detections with:
  - Current system timestamp.
  - Video time (seconds from start).
- Saving of raw and processed frames:
  - **`content/streamed_frames/`** – Raw frames extracted by the streamer.
  - **`content/final_results/`** – Processed frames with rectangles and timestamps.
- Multi-process architecture using queues for communication.
- Automatic pipeline start when a new video is added to `content/videos/`.
- Clean shutdown when video ends.

---

## Project Structure



## Project Structure

project/
├── streamer.py
├── detector.py
├── displayer.py
├── watcher.py # Watches folder for new videos
├── utils/
│ └── detect_func.py
├── main.py # Main pipeline entry
├── content/
│ ├── videos/ # Input videos
│ ├── streamed_frames/ # Raw extracted frames
│ └── final_results/ # Processed frames with rectangles + timestamps
├── processed_frames/ # (Optional extra folder)
└── README.md

Automatic run with Watchdog

Run the watcher to monitor content/videos for new videos:

python whatchdog_new_content.py


The pipeline will start automatically when a new video is added to the folder.

Multiple videos can be processed independently if more files appear.