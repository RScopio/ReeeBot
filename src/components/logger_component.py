import os
import sys
import atexit
import datetime
import time

class Logger:
    def __init__(self):
        self.log_file = None

    def on_exit(self):
        if self.log_file:
            self.log_file.close()

    def start(self):
        # initialize log file
        if not os.path.exists('logs'):
            os.makedirs('logs')
        log_file_path = os.path.join('logs', datetime.datetime.now().strftime("%Y-%m-%d") + '.txt')
        self.log_file = open(log_file_path, "a")
        sys.stdout = self.log_file
        atexit.register(self.on_exit)

    def tprint(self, *args, **kwargs):
        print(time.strftime("[%Y-%m-%d %H:%M:%S]"), *args, **kwargs)
