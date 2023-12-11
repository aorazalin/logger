from log_component.log_component import LogComponent

import time
import random

class Application:
    def __init__(self, log):
        self._log = log

    def run(self):
        # Simulate application logic that generates log messages
        for i in range(20):
            self._log.write(f"Log message {i}")
            time.sleep(random.uniform(0.1, 0.5))

    def stop(self, wait_for_outstanding_logs: bool):
        self._log.stop(wait_for_outstanding_logs)

def main():
    log_component = LogComponent()
    app = Application(log_component)

    try:
        print("Starting the application...")
        app.run()
    finally:
        print("Stopping the application...")
        app.stop(wait_for_outstanding_logs=True)
        print("Application stopped.")

if __name__ == "__main__":
    main()