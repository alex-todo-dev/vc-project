from env_loader import MAIN_PIPELINE_MODULE_NAME
from env_loader import FRAME_STREAM_QUEUE_SIZE
from env_loader import DETECTED_FRAMES_QUEUE_SIZE
from env_loader import DETECTOR_WORKER_COUNT
from multiprocessing import Process, Queue
from steamer import frame_streamer
from detector import detect_objects
from displayer import display_process



def start_main_pipeline(video_path: str) -> dict:
    print(f'[{MAIN_PIPELINE_MODULE_NAME}] Main pipeline staring process...')

    # SETUP QUEUES
    # frame_queue = Queue(maxsize=int(FRAME_STREAM_QUEUE_SIZE))
    frame_queue = Queue() # for development purposes, no max size
    # frame_queue = Queue(maxsize=int(DETECTED_FRAMES_QUEUE_SIZE))
    processed_frames_queue = Queue() # for development purposes, no max size

    # PROCESS SETUP
    frame_streamer_process = Process(target=frame_streamer, args=(video_path, frame_queue))
    display_process_process = Process(target=display_process, args=(processed_frames_queue,))

    detect_workers = []
    

    # START PROCESSES
    display_process_process.start()
    
    for worker_id in range(int(DETECTOR_WORKER_COUNT)):
        detect_worker = Process(target=detect_objects, args=(frame_queue, processed_frames_queue, worker_id))
        detect_worker.start()
        print(f'[{MAIN_PIPELINE_MODULE_NAME}] Detector worker {worker_id} started.')
        detect_workers.append({"worker_id": worker_id, "process": detect_worker})
    

    frame_streamer_process.start()

    # Wait for the frame streamer process to finish
    frame_streamer_process.join()

    print (f'[{MAIN_PIPELINE_MODULE_NAME}] Vide processing completed for: {video_path}')
    
    return {"status": "success", "message": f'[{MAIN_PIPELINE_MODULE_NAME}] Video processing completed for: {video_path}'}



if __name__ == "__main__":
    video_path = "content/videos/People - 6387.mp4"
    start_main_pipeline(video_path)

