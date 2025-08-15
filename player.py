import cv2
import os
import time
# from env_loader import RESULTS_FRAME_FOLDER

def play_saved_frames(folder_path, delay=0.03):
    """
    Displays saved frames from the given folder in sequence.

    Args:
        folder_path (str): Path to folder containing .jpg frames.
        delay (float): Delay between frames in seconds (e.g., 0.03 for ~30 FPS).
    """
    if not os.path.exists(folder_path):
        print(f"[ERROR] Folder '{folder_path}' not found.")
        return
    
    # Get all jpg files
    frame_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".jpg")]
    if not frame_files:
        print(f"[INFO] No .jpg files found in '{folder_path}'.")
        return
    
    # Sort by numeric frame ID (if filenames are like frame_0001.jpg)
    frame_files.sort(key=lambda x: int("".join(filter(str.isdigit, x)) or 0))
    
    print(f"[INFO] Playing {len(frame_files)} frames from '{folder_path}'...")

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