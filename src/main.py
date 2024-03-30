#!/usr/bin/env python3

import sys
import os
import discord
from discord import Intents
import atexit
import datetime
from dotenv import load_dotenv
import response_controller
import command_controller

def on_exit():
    log_file.close()

# load environment variables
if os.name == 'nt':
    TOKEN = os.getenv('DISCORD_TOKEN')
else:
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

if TOKEN is None:
    print('DISCORD_TOKEN not found')
    exit(1)

# initialize discord client
intents = Intents.default()
client = discord.Client(intents=intents)

# initialize log file
if not os.path.exists('logs'):
    os.makedirs('logs')
log_file = open('logs/' + datetime.datetime.now().strftime("%Y-%m-%d") + '.txt', "a")
sys.stdout = log_file
atexit.register(on_exit)

# initialize controllers
@client.event
async def on_ready():
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'Mother give me tendies')

@client.event
async def on_message(message: discord.Message):
    await response_controller.scan_message(message)
    await command_controller.scan_message(message)

client.run(TOKEN)
