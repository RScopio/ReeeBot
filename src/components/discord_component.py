import os
import datetime
import discord
from discord import Intents
from dotenv import load_dotenv
from components import language_component

def start():
# load environment variables
    dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    load_dotenv(dotenv_path, override=True)
    TOKEN = os.getenv('DISCORD_TOKEN')
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'DISCORD_TOKEN: ' + str(TOKEN))
    if TOKEN is None:
        print('DISCORD_TOKEN not found')
        exit(1)

    # initialize discord client
    intents = Intents.default()
    client = discord.Client(intents=intents)

    # event handlers
    @client.event
    async def on_ready():
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'Mother give me tendies')

    @client.event
    async def on_message(message: discord.Message):

        # ignore messages from the bot itself
        if message.author == client.user:
            return

        # read the last 13 messages from the channel
        recent_messages = [msg async for msg in message.channel.history(limit=69)]

        # squash messages into a single string
        recent_messages.reverse()
        recent_messages = [f"{msg.author.name}: {msg.content}" for msg in recent_messages]
        recent_messages = "\n".join(recent_messages)

        # generate response
        response = language_component.generate_response(recent_messages)

        # trim response to 2000 characters
        response = response[:2000]
        await message.channel.send(response)
        
    client.run(TOKEN)
