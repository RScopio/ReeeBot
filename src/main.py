#!/usr/bin/env python3

import sys
import os
import discord
import atexit
import datetime
from dotenv import load_dotenv
import response_controller
import command_controller

def on_exit():
    log_file.close()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

if TOKEN is None:
    print('DISCORD_TOKEN not found')
    exit(1)

client = discord.Client()
log_file = open('logs/' + datetime.datetime.now().strftime("%Y-%m-%d") + '.txt', "a")
sys.stdout = log_file
atexit.register(on_exit)

@client.event
async def on_ready():
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'Mother give me tendies')

@client.event
async def on_message(message: discord.Message):
    await response_controller.scan_message(message)
    await command_controller.scan_message(message)

client.run(TOKEN)
