import asyncio
import os
import datetime
import discord
from discord import Intents
from discord import app_commands
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
    tree = app_commands.CommandTree(client)

    @tree.command(name='speak', description='Generate a response from the AI model.')
    async def speak(interaction):
        """Generate a response from the AI model."""
        
        await interaction.response.defer()

        # read the last 69 messages from the channel
        recent_messages = [msg async for msg in interaction.channel.history(limit=69)]
        recent_messages.reverse()
        recent_messages = [f"{msg.author.name}: {msg.content}" for msg in recent_messages]
        recent_messages = "\n".join(recent_messages)

        # generate response
        response = language_component.generate_response(recent_messages)
        response = response[:2000]
        
        await interaction.followup.send(content=response)

    # event handlers
    @client.event
    async def on_ready():
        await tree.sync()
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'Mother give me tendies')

    @client.event
    async def on_message(message: discord.Message):
        # ignore messages from the bot itself
        if message.author == client.user:
            return

    client.run(TOKEN)
