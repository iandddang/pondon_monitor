import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
from settings import config
import monitor

# initializes discord client
Client = discord.Client()
client = commands.Bot(command_prefix = "!")

firstMonitor = False

# event handler
@client.event
async def on_ready():
    await client.send_message(client.get_channel(config.channel_id), "U N D E R W A T E R S Q U A D")
    monitor.check(config.baseURL)
    firstMonitor = True

client.run(config.bot_token)
