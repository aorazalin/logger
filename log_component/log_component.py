import threading
import os
import time
from datetime import datetime
from queue import Queue
from typing import Optional

from datetime import datetime
from abc import ABC, abstractmethod

class ILog(ABC):
    @abstractmethod
    def write(self, message: str):
        pass

    @abstractmethod
    def stop(self, wait_for_outstanding_logs: bool):
        pass

class LogComponent:
    def __init__(self, max_file_size: int = 10 * 1024 * 1024):
        self.max_file_size = max_file_size
        self.log_queue = Queue()
        self.lock = threading.Lock()
        self.stop_event = threading.Event()
        self.worker_thread = threading.Thread(target=self._worker)
        self.worker_thread.start()

    def write(self, message: str):
        current_time = datetime.now()
        log_entry = (current_time, message)
        self.log_queue.put(log_entry)

    def stop(self, wait_for_outstanding_logs: bool):
        if wait_for_outstanding_logs:
            self.log_queue.join()
        self.stop_event.set()
        self.worker_thread.join()

    def _worker(self):
        while not self.stop_event.is_set() or not self.log_queue.empty():
            try:
                log_entry = self.log_queue.get(timeout=1)
            except Exception:
                continue

            timestamp, message = log_entry
            self._write_to_file(timestamp, message)
            self.log_queue.task_done()

    def _write_to_file(self, timestamp: datetime, message: str):
        with self.lock:
            filename = self._get_filename(timestamp)
            with open(filename, "a") as file:
                file.write(f"{timestamp}: {message}\n")
                file.flush()

            if os.path.getsize(filename) > self.max_file_size:
                self._rotate_file(filename)

    def _get_filename(self, timestamp: datetime) -> str:
        return f"log_{timestamp.strftime('%Y%m%d')}.txt"

    def _rotate_file(self, filename: str):
        i = 1
        while os.path.exists(f"{filename[:-4]}_{i}.txt"):
            i += 1
        os.rename(filename, f"{filename[:-4]}_{i}.txt")