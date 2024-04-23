import asyncio
import os
import datetime
from . import logger_component
import discord
from discord import app_commands
from dotenv import load_dotenv
from components import language_component

def start(logger):
    logger.tprint('Starting Discord component...')
    
    # load environment variables
    dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    load_dotenv(dotenv_path, override=True)
    TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD_IDS = os.getenv('DISCORD_GUILD_IDS')
    if TOKEN is None or GUILD_IDS is None:
        logger.tprint('DISCORD_TOKEN or DISCORD_GUILD_IDS not found')
        exit(1)
    else:
        logger.tprint('DISCORD_TOKEN and DISCORD_GUILD_IDS found')

    GUILD_IDS = [int(guild_id) for guild_id in GUILD_IDS.split(",")]

    # initialize discord client
    client = discord.Client(intents=discord.Intents.default())
    tree = discord.app_commands.CommandTree(client)

    # bot slash commands
    @tree.command(name="ping", description="Sends the bot's latency.")
    async def ping(interaction): 
        logger.tprint('ping command called')
        await interaction.response.send_message(f"Pong! Latency is {client.latency}")

    @tree.command(name="speak", description="Generate a response from the AI model.")
    async def speak(interaction, prompt: str):
        logger.tprint('speak command called: ' + prompt)
        await interaction.response.defer()

        # generate response
        output = language_component.generate_response(prompt)
        response = "> " + f"<@{interaction.user.display_name}>: " + prompt + "\n\n" + output
        
        # follow up with response
        response = response[:2000]
        await interaction.followup.send(response)

    @client.event
    async def on_ready():
        await tree.sync()
        logger.tprint(f'{client.user} has connected to Discord!')

    client.run(TOKEN)
