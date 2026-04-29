#!/usr/bin/env python3

import os
import time
import zipfile
import sys
# import logging
# from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver
# from watchdog.events import LoggingEventHandler
# from pathlib import Path
from watchdog.events import FileSystemEventHandler

# Use line buffering so output shows up immediately when piped to tee.
sys.stdout.reconfigure(line_buffering=True)

# This should watch for filesystem events in my Downloads directory.

DOWNLOADS_PATH = "/mnt/c/Users/jadea/Downloads"

class ZipFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        file_path = event.src_path
        if file_path.lower().endswith(".zip"):
            # Small delay to ensure the file is fully written/downloaded
            time.sleep(1.5)
            self.smart_extract(file_path)

    def is_single_folder(self, zip_ref):
        """Checks if all items in the zip are contained within one top-level directory."""
        members = zip_ref.namelist()
        if not members:
            return False

        # Get the first part of the first file path (the potential top-level folder)
        top_level = members[0].split('/')[0]

        # Check if every single entry starts with that same top-level folder name
        return all(m.split('/')[0] == top_level for m in members)

    def smart_extract(self, file_path):
        # Default destination is the Downloads folder itself
        dest_dir = DOWNLOADS_PATH
        zip_name = os.path.basename(file_path)

        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                if not self.is_single_folder(zip_ref):
                    # If it's a "messy" zip, create a dedicated folder named after the zip.
                    new_folder_name = os.path.splitext(zip_name)[0]
                    dest_dir = os.path.join(DOWNLOADS_PATH, new_folder_name)

                    if not os.path.exists(dest_dir):
                        os.makedirs(dest_dir)
                    print(f"Flat ZIP detected. Creating directory: {new_folder_name}.")
                else:
                    print(f"Nested ZIP detected. Extracting directly to Downloads.")

                zip_ref.extractall(dest_dir)
                print(f"Successfully extracted {zip_name} to {dest_dir}.")

        except Exception as e:
            print(f"Error processing {zip_name}: {e}")

if __name__ == "__main__":
    event_handler = ZipFileHandler()
    observer = PollingObserver()
    observer.schedule(event_handler, DOWNLOADS_PATH, recursive=False)

    print(f"Monitoring {DOWNLOADS_PATH} for new .zip files...")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopping...")

    observer.join()


