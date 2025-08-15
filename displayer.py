# displayer.py
import cv2
import time
import numpy as np
from multiprocessing import Queue
from env_loader import DISSPLAY_MODULE_NAME
from env_loader import RESULTS_FRAME_FOLDER
import os

# Optional: toggle blurring
APPLY_BLUR = True

# window_name = "Video Pipeline Display"
# cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

def display_process(input_queue: Queue) -> None:

    print(f"[{DISSPLAY_MODULE_NAME}] Starting display process...")
    while True:
        frame_data = input_queue.get()

        if frame_data is None:
                # Sentinel to stop process
                print(f"[{DISSPLAY_MODULE_NAME}] End of stream received. Stopping detection process.")
                break
        

        print(f"[{DISSPLAY_MODULE_NAME}] Received data: {frame_data.get('frame_id')}")

        frame = frame_data["frame"]
        detections = frame_data.get("detections", [])
        video_time_sec = frame_data.get("video_time_sec", 0.0)

        # Draw detections (rectangles)
        # Blur or draw rectangles on detections
        for (x, y, w, h) in detections:
            if APPLY_BLUR:
                # Extract region of interest (ROI)
                roi = frame[y:y+h, x:x+w]
                # Apply Gaussian blur to ROI
                blurred_roi = cv2.GaussianBlur(roi, (25, 25), 0)
                # Replace original region with blurred
                frame[y:y+h, x:x+w] = blurred_roi
            else:
                # Just draw rectangle if blur not enabled
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Add timestamp (top-left corner)
        timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, timestamp_str, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # Add video time in seconds (below timestamp)
        video_time_str = f"Video Time: {video_time_sec:.2f}s"
        cv2.putText(frame, video_time_str, (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
        
        # # Play resulst
        # cv2.imshow(window_name, frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        
         # Save frame to disk
        frame_filename = os.path.join(RESULTS_FRAME_FOLDER, f"frame_{frame_data['frame_id']:05d}.jpg")
        cv2.imwrite(frame_filename, frame)

        

    print(f"[{DISSPLAY_MODULE_NAME}] Display process finished.")


