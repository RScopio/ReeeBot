import asyncio
import os
import datetime
import discord
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv
from components import language_component

def start():
    print('Starting Discord component...')
    
    # load environment variables
    dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    load_dotenv(dotenv_path, override=True)
    TOKEN = os.getenv('DISCORD_TOKEN')
    if TOKEN is None:
        print('DISCORD_TOKEN not found')
        exit(1)
    else:
        print('DISCORD_TOKEN found')

    # initialize discord client
    bot = discord.Bot()

    # bot slash commands
    @bot.command(name="ping", description="Sends the bot's latency.")
    async def ping(ctx): 
        print('ping command called')
        await ctx.respond(f"Pong! Latency is {bot.latency}")

    @bot.command(name="speak", description="Generate a response from the AI model.")
    async def speak(ctx, prompt: discord.Option(str)):
        print('speak command called')
        await ctx.response.defer()
        # generate response
        response = language_component.generate_response(prompt)
        response = response[:2000]
        # follow up with response
        await ctx.followup.send(response)

    bot.run(TOKEN)
