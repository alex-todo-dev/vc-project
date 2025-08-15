from env_loader import DETECTOR_MODULE_NAME
from multiprocessing import Process, Queue
from utils_funcs import detect_func
import copy
import numpy as np

    #  # Frame data 
    #     frame_data = {
    #         "frame_id": frame_id,
    #         "frame_extract_ts": frame_extract_ts,
    #         "video_time_sec": video_time_sec,
    #         "frame": frame
    #     }

def detect_objects(input_queue: Queue, output_queue: Queue, worker_id:str) -> dict:
    print(f"[{DETECTOR_MODULE_NAME}] Starting object detection process...")

    prev_frame = None
    frame_counter = 0

    while True:
        print("***********************************************************")
        try: 
            frame_data = input_queue.get()  

            # If frame_data is None, it indicates the end of the stream
        
            if frame_data.get("end_of_stream"):
                # Sentinel to stop process
                print(f"[{DETECTOR_MODULE_NAME}] End of stream received. Stopping detection process.")
                output_queue.put(None)
                break
            
            # Print frame data 
            # print(f"[DETECTOR_MODULE_NAME] frame_data: {frame_data}")
            # Process the frame data
            frame_id = frame_data["frame_id"]
            frame = frame_data["frame"]

            # check both frames are not same 

            print(f"[{DETECTOR_MODULE_NAME}]Check both frames are not same:", np.array_equal(prev_frame, frame))

            detections = []
            # Run detection (returns list of bounding boxes)
            if prev_frame is not None:
                print(f"[{DETECTOR_MODULE_NAME}] Processing frame ID: {frame_id}, worker ID: {worker_id}")
                detections = detect_func.detect_motion(prev_frame, frame)
                print(f"[{DETECTOR_MODULE_NAME}] Detections for frame ID {frame_id}: comppleted")
                print(f"[{DETECTOR_MODULE_NAME}] Found detections: {len(detections)}")
                
            
            # Update the previous frame
            prev_frame = frame.copy()
            frame_counter += 1

            # If no detections found, continue to the next frame
            if len(detections) > 0:     
                # Prepare the output data with detections
                output_data = copy.deepcopy(frame_data) # new reference
                output_data["detections"] = detections

                # Send the processed frame data to the output queue
                output_queue.put(output_data)
            print(f"[{DETECTOR_MODULE_NAME}] Current output queue size: {output_queue.qsize()}")
        except Exception as e:  
            print(f"[{DETECTOR_MODULE_NAME}] Error getting frame data from input queue: {e}")
            continue


if __name__ == "__main__":
    # Call the function to detect objects
    input_queue = Queue()
    output_queue = Queue()
    detect_objects(input_queue=input_queue, output_queue=output_queue)