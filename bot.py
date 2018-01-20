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
    await client.send_message(client.get_channel(config.channel_id), "Hi there.\n\nRestock bot started.")


@client.command()
async def update():
    # define generator function
    # next keyword grabs the returned yield value and the program keeps on running
    # https://stackoverflow.com/questions/1756096/understanding-generators-in-python


    while firstMonitor is True:
        await client.send_message(client.get_channel(config.channel_id), "Now searching for restocks. No commands will work.")
        updateFxn = monitor.update(config.baseURL)
        # iterates through yielded values of updatefxn
        # only yields value on event
        for event in updateFxn:
            await client.send_message(client.get_channel(config.channel_id), event)
    else:
        await client.send_message(client.get_channel(config.channel_id),"Execute !begin first and wait for it to finish.")
        time.sleep(1)

@client.command()
async def begin():
    # ensures the firstMonitor instance being edited is the global variable
    global firstMonitor

    await client.send_message(client.get_channel(config.channel_id), "Initializing item dictionary. Please wait, no commands will work during this period.")
    monitor.check(config.baseURL)
    await client.send_message(client.get_channel(config.channel_id), "Item dictionary initialized.")
    firstMonitor = True

@client.command()
async def test():
    global firstMonitor
    firstMonitor = True

client.run(config.bot_token)
