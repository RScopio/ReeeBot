#!/usr/bin/env python3

import sys
import os
import atexit
import datetime
from components import discord_component

def on_exit():
    log_file.close()

# initialize log file
if not os.path.exists('logs'):
    os.makedirs('logs')
log_file_path = os.path.join('logs', datetime.datetime.now().strftime("%Y-%m-%d") + '.txt')
log_file = open(log_file_path, "a")
sys.stdout = log_file
atexit.register(on_exit)

discord_component.start()
