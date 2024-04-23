import asyncio
import os
import datetime
from . import logger_component
import discord
from discord import app_commands
from dotenv import load_dotenv
from components import language_component

class DiscordComponent:
    def __init__(self, logger):
        self.logger = logger
        self.client = None
        self.tree = None

    def load_env_vars(self):
        dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
        load_dotenv(dotenv_path, override=True)
        TOKEN = os.getenv('DISCORD_TOKEN')
        GUILD_IDS = os.getenv('DISCORD_GUILD_IDS')
        if TOKEN is None or GUILD_IDS is None:
            self.logger.tprint('DISCORD_TOKEN or DISCORD_GUILD_IDS not found')
            exit(1)
        else:
            self.logger.tprint('DISCORD_TOKEN and DISCORD_GUILD_IDS found')
        GUILD_IDS = [int(guild_id) for guild_id in GUILD_IDS.split(",")]
        return TOKEN, GUILD_IDS

    def initialize_client(self, TOKEN, GUILD_IDS):
        self.client = discord.Client(intents=discord.Intents.default())
        self.tree = discord.app_commands.CommandTree(self.client)

    def register_commands(self):
        @self.tree.command(name="ping", description="Sends the bot's latency.")
        async def ping(interaction): 
            self.logger.tprint('ping command called')
            await interaction.response.send_message(f"Pong! Latency is {self.client.latency}")

        @self.tree.command(name="speak", description="Generate a response from the AI model.")
        async def speak(interaction, prompt: str):
            self.logger.tprint('speak command called: ' + prompt)
            await interaction.response.defer()

            # generate response
            output = language_component.generate_response(prompt)
            response = "> " + f"<@{interaction.user.display_name}>: " + prompt + "\n\n" + output
            
            # follow up with response
            response = response[:2000]
            await interaction.followup.send(response)

    def register_events(self):
        @self.client.event
        async def on_ready():
            await self.tree.sync()
            self.logger.tprint(f'{self.client.user} has connected to Discord!')

    def start(self):
        self.logger.tprint('Starting Discord component...')
        TOKEN, GUILD_IDS = self.load_env_vars()
        self.initialize_client(TOKEN, GUILD_IDS)
        self.register_commands()
        self.register_events()
        self.client.run(TOKEN)