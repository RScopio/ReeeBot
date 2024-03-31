#!/usr/bin/env python3

import sys
import os
import discord
from discord import Intents
import atexit
import datetime
from dotenv import load_dotenv
from controllers import response_controller, command_controller

def on_exit():
    log_file.close()

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# initialize log file
log_dir = os.path.join(parent_dir, 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
log_file_path = os.path.join(log_dir, datetime.datetime.now().strftime("%Y-%m-%d") + '.txt')
log_file = open(log_file_path, "a")
sys.stdout = log_file
atexit.register(on_exit)

# load environment variables
load_dotenv(os.path.join(parent_dir, '.env'), override=True)
TOKEN = os.getenv('DISCORD_TOKEN')
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'DISCORD_TOKEN: ' + str(TOKEN))
if TOKEN is None:
    print('DISCORD_TOKEN not found')
    exit(1)

# initialize discord client
intents = Intents.default()
client = discord.Client(intents=intents)

# initialize controllers
@client.event
async def on_ready():
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'Mother give me tendies')

@client.event
async def on_message(message: discord.Message):
    await response_controller.scan_message(message)
    await command_controller.scan_message(message)

client.run(TOKEN)
