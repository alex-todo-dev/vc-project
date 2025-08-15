from env_loader import FRAME_STREAM_MODULE_NAME
from env_loader import GENERATED_FRAMES_FOLDER
from multiprocessing import Process, Queue
import cv2
import time 
import os


def frame_streamer(video_path: str, out_put_frames_queue: Queue) -> dict:
    print(f'[{FRAME_STREAM_MODULE_NAME}] Starting frame streaming for {video_path}...')

    # Open the video file
    try:
        video_meta_data = cv2.VideoCapture(video_path)
    except Exception as e:
        print(f'[{FRAME_STREAM_MODULE_NAME}] Error opening video file: {e}')
        return {"status": "error", "message": f'[{FRAME_STREAM_MODULE_NAME}] Failed to open video file.'}
    
    # Extract frames from the video data 
    frame_per_sec =  video_meta_data.get(cv2.CAP_PROP_FPS)
    frames_count = int(video_meta_data.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f'[{FRAME_STREAM_MODULE_NAME}] Video FRAMES_PER_SEC: {frame_per_sec}, total_frames:{frames_count}')

    # delay between frames pull (Sync with detector)- Optional 
    delay_new_frame_pull = 1.0 / frames_count

    frame_id = 0

    # For testing low frames count
    test_frame_count = 100

    # Process frames until the end of the video
    while True:
        ret, frame = video_meta_data.read()
        if not ret:
            print(f'[{FRAME_STREAM_MODULE_NAME}] No more frames to read.')
            break
        if frame_id >= test_frame_count:
            print(f'[{FRAME_STREAM_MODULE_NAME}] Reached test frame count limit: {test_frame_count}. Stopping frame extraction.')
            break
        # Frame extract timestamp 
        frame_extract_ts = time.time()

        # Frame time in the video
        video_time_sec = video_meta_data.get(cv2.CAP_PROP_POS_MSEC) / 1000.0

        # Frame data 
        frame_data = {
            "frame_id": frame_id,
            "frame_extract_ts": frame_extract_ts,
            "video_time_sec": video_time_sec,
            "frame": frame
        }

        # Put the frame data into the output queue
        out_put_frames_queue.put(frame_data)

        # Save frame for check - OPTIONAL for dev
        frame_filename = os.path.join(GENERATED_FRAMES_FOLDER, f"frame_{frame_id:04d}.jpg")
        cv2.imwrite(frame_filename, frame)

        frame_id += 1
        # Deplay to sync with detector
        time.sleep(delay_new_frame_pull)  

    # Release the video capture object
    out_put_frames_queue.put({"end_of_stream": True})
    video_meta_data.release()

    print(f'[FRAME_STREAM_MODULE_NAME] Queue size: {out_put_frames_queue.qsize()}')

    return {"status": "success", "message": f'[{FRAME_STREAM_MODULE_NAME}] Streaming frames from {video_path} completed.'}


if __name__ == "__main__":
    frame_queue = Queue()
    video_path = "content/videos/People - 6387.mp4"
    frame_streamer(video_path, frame_queue)
    