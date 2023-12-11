from log_component import ILog, LogComponent
import unittest
import os
import time

class TestLogComponent(unittest.TestCase):

    def setUp(self):
        self.log_component = LogComponent()

    def tearDown(self):
        self.log_component.stop(wait_for_outstanding_logs=True)

    def test_write_to_file(self):
        message = "Test log message"
        self.log_component.write(message)

        # Give the worker thread some time to process the log message
        time.sleep(1)

        # Get the expected log file name
        timestamp = time.localtime()
        expected_filename = f"log_{time.strftime('%Y%m%d', timestamp)}.txt"

        # Check if the log file exists and contains the log message
        self.assertTrue(os.path.exists(expected_filename))

        with open(expected_filename, "r") as file:
            file_contents = file.read()
            self.assertIn(message, file_contents)

if __name__ == '__main__':
    unittest.main()

