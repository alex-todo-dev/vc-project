from watchdog.observers import Observer 
from watchdog.events import FileSystemEventHandler
from main_pipeline import start_main_pipeline
from env_loader import MP4_VIDEO_CONTENT_FOLDER
from env_loader import WHATCH_MODULE_NAME
import time 

# Watchdog module to monitor new video content and trigger processing
class VideoFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".mp4"):

            print(f"[{WHATCH_MODULE_NAME}] New video detected: {event.src_path}")

            # Delay to ensure the file is fully written
            time.sleep(1)
            
            # Start the main processing pipeline for the new video
            start_main_pipeline(event.src_path)

# Watchdog module to monitor new video content in a specified folder
def watch_folder(content_path):
    event_hendler = VideoFileHandler()
    observer = Observer()
    observer.schedule(event_hendler, content_path, recursive=False)
    observer.start()
    print(f'[{WHATCH_MODULE_NAME}] Watching folder: {content_path}')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    print("Event folder:", MP4_VIDEO_CONTENT_FOLDER)
    watch_folder(MP4_VIDEO_CONTENT_FOLDER)