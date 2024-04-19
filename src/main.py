#!/usr/bin/env python3

from components import logger_component
from components import discord_component

logger = logger_component.Logger()
logger.start()

discord_component.start(logger)
