# imports
import os
import random
import time
import asyncio
import keyboard
import sys
import numpy as np

import discord
from discord.ext.commands import Bot
from discord.ext import commands

class definement:
    def __init__(self):
        # global var definement
        self.Admins = [554486518543155212, 315311722321936385, 319257037597048832] 
        self.client = discord.Client()
        self.Prefix = 'ad.'
        intents = discord.Intents.default()
        intents.members = True
        self.bot = commands.Bot(command_prefix='ad.', description="bot")
        self.ticker = 0
        self.servers = []

        self.advertisment = ["https://cdn.discordapp.com/attachments/809861589485355099/819595039306022943/Free_Candy.png",
                             "https://cdn.discordapp.com/attachments/809861589485355099/819595040904577084/Tree_prefume.png",
                             "https://cdn.discordapp.com/attachments/809861589485355099/819595042712191027/bigdaddy.png",
                             "https://cdn.discordapp.com/attachments/798208632386879490/819662895562227793/butter.png",
                             "https://cdn.discordapp.com/attachments/809861589485355099/819604550092324875/photoshop.png",
                             "https://cdn.discordapp.com/attachments/809861148706078751/819607484372353054/becomepirate.png",
                             "https://cdn.discordapp.com/attachments/797947840507805709/819608418510962728/thismanisgay.png",
                             "https://cdn.discordapp.com/attachments/797947840507805709/819614385676222554/MargretThatcher.jpg"]
        self.addfreq = 50
        self.adsendcheck = True
        self.adchannel = 819611597118504980
        self.ad_ids = []
        self.reacted = [[None, None]]


d = definement()





@d.client.event
async def sendAd(message):
    # sends the advertisements that had been created in definement
    if d.adsendcheck:
        d.adsendcheck = False
    for server in d.servers:

        if message.guild.id == server[0]:
            adchannel = d.client.get_channel(server[2])
            continue
    admessage = await adchannel.send(d.advertisment[random.randint(0,len(d.advertisment) - 1)])
    await admessage.add_reaction("👍")
    d.ad_ids.append(admessage.id)



@d.client.event
async def on_raw_reaction_add(payload):
    global admessage

    if payload.message_id in d.ad_ids and payload.user_id != 813464276240564284:
        for arrays in d.reacted:
            if payload.user_id == arrays[1]:
                return
        d.reacted.append([payload.message_id, payload.user_id])
        for server in d.servers:
            if payload.guild_id == server[0]:
                server[4] += 0.11

                return

@d.client.event
async def on_ready():
    # typical boot sequence, also creates a 2d array for each server the bot is in
    for server in d.client.guilds:
        d.servers.append([d.client.guilds[d.ticker].id, 0, d.adchannel, 50, 0.00])
        d.ticker += 1
    user = ("{0.user}".format(d.client))
    channel = d.client.get_channel(809861589485355099)
    await channel.send((f"```\n\nBot online logged in as {user} \n"
                       f"\nDiscord> {discord.__version__} {discord.version_info}"
                       f" \t|||\tKeyboard> {keyboard.version}"
                       f"\t|||\nPython> {sys.version}/{sys.version_info}```"))
    print("bot online")

@d.bot.command()
@d.client.event
async def on_message(message):
    if message.author == d.client.user:
        return

    print(f"Servers: {d.servers}")
    print(f"Ad ids: {d.ad_ids}")
    # checks where the message was sent and adds 1 to the ticker for that server
    for server in d.servers:

        if message.guild.id == server[0]:
            server[1] += 1

            if server[1] % server[3] == 0:
                await sendAd(message)

    if message.content == d.Prefix + "up":
        await message.channel.send("Currently online")

    elif message.content == d.Prefix + "sendad":
        await sendAd(message)
        print("ad sent")

    elif message.content.startswith(d.Prefix + "adchannel"):
        for server in d.servers:

            if message.guild.id == server[0]:
                null2 = server[2]
                server[2] = message.channel.id
                await message.channel.send(f"Old advert chat:{null2}\nNew advert chat:{server[2]}")

    elif message.content.startswith(f"{d.Prefix}adfreq"):
        for server in d.servers:

            if message.guild.id == server[0]:
                try:
                    null1 = server[3]
                    server[3] = int(message.content[len(d.Prefix) + 7: len(message.content)])
                    await message.channel.send(f"Old ad frequency: {null1}\nNew ad frequency: {server[3]}")
                except(ValueError):
                    await message.channel.send("Please include an int")
                    return
    
    elif message.content == d.Prefix + "wallet":
        for server in d.servers:
            if message.guild.id == server[0]:
                await message.channel.send(f"Your current balance is: {server[4]}")
                return

# runs the bot token (env var)
d.client.run(os.getenv("var1"))
