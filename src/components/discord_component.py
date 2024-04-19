import asyncio
import os
import datetime
from . import logger_component
import discord
from discord.ext import commands
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
    bot = discord.Bot()

    # bot slash commands
    @bot.command(name="ping", description="Sends the bot's latency.", guild_ids=GUILD_IDS)
    async def ping(ctx): 
        logger.tprint('ping command called')
        await ctx.respond(f"Pong! Latency is {bot.latency}")

    @bot.command(name="speak", description="Generate a response from the AI model.", guild_ids=GUILD_IDS)
    async def speak(ctx, prompt: discord.Option(str)):
        logger.tprint('speak command called: ' + prompt)
        await ctx.response.defer()

        # generate response
        output = language_component.generate_response(prompt)
        response = "> " + f"<@{ctx.author.id}>: " + prompt + "\n\n" + output
        
        # follow up with response
        response = response[:2000]
        await ctx.followup.send(response)

    bot.run(TOKEN)
