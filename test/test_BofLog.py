import sys
import os
# Add the parent directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import logging
import shutil
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from bofpy.BofLog import (                                                           
    BofLog
)
class TestBofLog(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for log files
        self.log_dir = "temp_logs"
        try:
            shutil.rmtree(self.log_dir)
        except Exception as e:
            pass   
        os.makedirs(self.log_dir, exist_ok=True)

    def tearDown(self):
        # Clean up: Remove the temporary directory and its contents
        for handler in logging.getLogger().handlers[:]:
            logging.getLogger().removeHandler(handler)
        try:
            shutil.rmtree(self.log_dir)
        except Exception as e:
            pass   

    def test_set_log_level(self):
        bof_log = BofLog()
        bof_log.SetLogLevel(logging.DEBUG)

        self.assertEqual(logging.getLogger().getEffectiveLevel(), logging.DEBUG)
        for handler in bof_log.log_handler_collection:
            self.assertEqual(handler.getLevel(), logging.DEBUG)

        bof_log = BofLog()
        new_format = "%(asctime)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s"
        bof_log.SetLogFormat(new_format)

        self.assertEqual(logging.getLogger().handlers[0].formatter._fmt, new_format)
        for handler in bof_log.log_handler_collection:
            self.assertEqual(handler.formatter._fmt, new_format)

    def test_add_rotating_log(self):
        bof_log = BofLog()
        log_file = os.path.join(self.log_dir, "rotating_log.log")
        bof_log.AddRotatingLog(logging.DEBUG, log_file, max_file_size_bytes=1000, backup_count=3)

        # Check if the RotatingFileHandler is added to the logger
        self.assertIsInstance(logging.getLogger().handlers[0], logging.StreamHandler)
        self.assertIsInstance(logging.getLogger().handlers[1], RotatingFileHandler)
        self.assertEqual(len(bof_log.log_handler_collection), 1)
        self.assertIsInstance(bof_log.log_handler_collection[0], RotatingFileHandler)

        # Check if log messages are written to the log file
        bof_log.Debug("Debug message")
        self.assertTrue(os.path.exists(log_file))

    def test_add_timed_rotating_file_handler(self):
        bof_log = BofLog()
        log_file = os.path.join(self.log_dir, "timed_rotating_log.log")
        bof_log.AddTimedRotatingFileHandler(logging.DEBUG, log_file, when="D", interval=1, backup_count=3)

        # Check if the TimedRotatingFileHandler is added to the logger
        self.assertIsInstance(logging.getLogger().handlers[0], logging.StreamHandler)
        self.assertIsInstance(logging.getLogger().handlers[1], TimedRotatingFileHandler)
        self.assertEqual(len(bof_log.log_handler_collection), 1)
        self.assertIsInstance(bof_log.log_handler_collection[0], TimedRotatingFileHandler)

        # Check if log messages are written to the log file
        bof_log.Info("Info message")
        self.assertTrue(os.path.exists(log_file))

    def test_log_methods(self):
        bof_log = BofLog()

        # Test debug method
        bof_log.Debug("Debug message")
        # TODO: Check if the log message is written to the log handlers

        # Test info method
        bof_log.Info("Info message")
        # TODO: Check if the log message is written to the log handlers

        # Test warning method
        bof_log.Warning("Warning message")
        # TODO: Check if the log message is written to the log handlers

        # Test error method
        bof_log.Error("Error message")
        # TODO: Check if the log message is written to the log handlers

        # Test critical method
        bof_log.Critical("Critical message")
        # TODO: Check if the log message is written to the log handlers


if __name__ == "__main__":
    unittest.main()
