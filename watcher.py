import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from src.ingest import ingest_file

class KnowledgeBaseHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"New file detected: {event.src_path}")
            # Slight delay to ensure file write is complete
            time.sleep(1)
            ingest_file(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            print(f"File modified: {event.src_path}")
            time.sleep(1)
            ingest_file(event.src_path)

def start_watcher(path="./data"):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

    event_handler = KnowledgeBaseHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    print(f"Started watching {path} for new documents...")
    return observer
