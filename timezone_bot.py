# Author: Andrew Magana
# timezone_bot.py
import os

import discord
from dateutil import parser
from dotenv import load_dotenv
from pytz import timezone

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()


@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following GUILD:\n'
        f'{guild.name} (id: {guild.id})'
    )


# This is a method that takes in three parameters: trigger, entered time, and the target timezone.
# Once it is entered, it will spit back out the equivalent time in many timezones.
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    timezone_list = ['UTC', 'US/Pacific', 'Europe/Berlin', 'GMT', 'US/Eastern']

    print("INPUT: ", message.content.split())

    # Edge case
    if '!timezone' in message.content and len(message.content.split()[0]) != 10:
        await message.channel.send("Error! You dropped an 's'. Should be !timezones.")

    # Make sure if it is !timezones, only 3 values exist in array, otherwise error.
    if '!timezones' in message.content and len(message.content.split()[0]) == 10:

        if len(message.content.split()) > 3:
            # Edge case - They separated the time + am/pm.
            if "am" in message.content.split()[2] or "pm" in message.content.split()[2]:
                await message.channel.send("Error! You need to combine the am/pm to the time like: 4pm or 4:30pm")
                return
            else:
                # Edge case - too many params.
                await message.channel.send(
                    "Error! Too many parameters. Only three should be used: !timezones {time} {timezone}")
                return

        # Grab the params...
        trigger = message.content.split()[0]
        time_entered = message.content.split()[1]

        try:
            time_zone_source = message.content.split()[2].upper()
        except IndexError:
            time_zone_source = None
            await message.channel.send(
                "Error! You forgot to enter the timezone! Format should be: !timezones {time} {timezone}")

        try:
            current_time = parser.parse(time_entered + " " + time_zone_source)
        except ValueError:
            current_time = None
            await message.channel.send(
                "Error! Problem with the time string. Make sure it is in the format of: 4pm or 4:30pm")

        for zone in timezone_list:
            converted_times = current_time.astimezone(timezone(zone)).strftime("%H:%M%p %Z")
            await message.channel.send(converted_times)


client.run(TOKEN)
