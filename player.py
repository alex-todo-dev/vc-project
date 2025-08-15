import cv2
import os
import time
from env_loader import PLAYER_MODULE_NAME
# from env_loader import RESULTS_FRAME_FOLDER

def play_saved_frames(folder_path = '/home/alexander/vc-project/content/results_frames', delay=0.03):

    
    
    # Get all jpg files
    frame_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".jpg")]
   
    
    # Sort by numeric frame ID (if filenames are like frame_0001.jpg)
    frame_files.sort(key=lambda x: int("".join(filter(str.isdigit, x)) or 0))
    
    print(f"[{PLAYER_MODULE_NAME}] Playing {len(frame_files)} frames from '{folder_path}'...")

    for filename in frame_files:
        frame_path = os.path.join(folder_path, filename)
        frame = cv2.imread(frame_path)
        if frame is None:
            print(f"[WARNING] Could not read {frame_path}")
            continue

        cv2.imshow("Saved Video Playback", frame)
        if cv2.waitKey(int(delay * 1000)) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Absolute-safe relative path
    play_saved_frames('/home/alexander/vc-project/content/results_frames')