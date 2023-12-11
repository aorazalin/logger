from log_component import LogComponent

import time
import random

class Application:
    def __init__(self, log):
        self._log = log

    def run(self, start_number: int, stop_number: int, wait_for_outstanding_logs: bool):
        # Generate log messages with numbers going from start_number down to stop_number
        numrange = range(start_number, stop_number, 1) if stop_number > start_number else range(start_number, stop_number, -1)

        for i in numrange:
            self._log.write(f"Log message {i}")
            time.sleep(random.uniform(0.1, 0.5))

        # Stop the logging component with the specified wait_for_outstanding_logs parameter
        self._log.stop(wait_for_outstanding_logs)

def main():
    # First log component without waiting for outstanding logs
    app1 = Application(LogComponent(log_prefix="app1_"))
    print("Starting the first application...")
    app1.run(start_number=50, stop_number=0, wait_for_outstanding_logs=False)
    print("First application stopped.")

    time.sleep(2)  # Give some time for the worker thread to process remaining log messages

    # Second log component with waiting for outstanding logs
    app2 = Application(LogComponent(log_prefix="app2_"))
    print("Starting the second application...")
    app2.run(start_number=0, stop_number=15, wait_for_outstanding_logs=True)
    print("Second application stopped.")

if __name__ == "__main__":
    main()