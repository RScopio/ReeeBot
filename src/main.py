#!/usr/bin/env python3

from components.logger_component import Logger
from components.discord_component import DiscordComponent

logger = Logger()
logger.start()

discord_component = DiscordComponent(logger)
discord_component.start()
