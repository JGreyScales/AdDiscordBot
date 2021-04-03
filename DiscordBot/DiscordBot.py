# imports
import os, random, time, asyncio, keyboard, sys

import discord
from discord.ext import commands
from discord.ext.commands import Bot


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
        self.adfreq = 50
        self.adsendcheck = True
        self.adchannel = 819611597118504980
        self.ad_ids = []
        self.reacted = [[None, None]]

# creates definements
d = definement()

@d.client.event
async def sendAd(message):
    # sends the advertisements that had been created in definement
    if d.adsendcheck:
        d.adsendcheck = False
    for server in d.servers:
        # checks to see which server it needs to send the ad to
        if message.guild.id == server[0]:
            adchannel = d.client.get_channel(server[2])
    # sends the ad
    admessage = await adchannel.send(d.advertisment[random.randint(0,len(d.advertisment) - 1)])
    await admessage.add_reaction("👍")
    d.ad_ids.append(admessage.id)



@d.client.event
# watches for reactions on advertisements 
async def on_raw_reaction_add(payload):
    # checks to see that the image being reacted to was created by the bot
    if payload.message_id in d.ad_ids and payload.user_id != 813464276240564284:
        print("reaction recieved\n")
        # checks logics for if the user has already reacted to that message
        for arrays in d.reacted:
            if payload.user_id == arrays[1] and payload.message_id == arrays[0]:
                return
        # adds to the wallet and appends the id to the array
        d.reacted.append([payload.message_id, payload.user_id])
        for server in d.servers:
            if payload.guild_id == server[0]:
                server[4] += server[5]

@d.client.event
async def on_ready():
    # typical boot sequence, also creates a 2d array for each server the bot is in
    for server in d.client.guilds:
        # stores as follows d.server.append([server name, server ticker, advertisement channel, ad frequency, current wallet, how much the owner gains per view])
        d.servers.append([d.client.guilds[d.ticker].id, 0, d.adchannel, 50, 0.00, 0.03])
        d.ticker += 1
    # creates a simple boot display
    user = ("{0.user}".format(d.client))
    channel = d.client.get_channel(809861589485355099)
    await channel.send((f"```\n\nBot online logged in as {user} \n"
                       f"\nDiscord> {discord.__version__} {discord.version_info}"
                       f" \t|||\tKeyboard> {keyboard.version}"
                       f"\t|||\nPython> {sys.version}/{sys.version_info}```"))
    print("bot online")

async def displayhelpembed(channel):
    #creates help embed
    embed = discord.Embed(title="Help", description=f"Prefix:{d.Prefix}")
    embed.set_author(name="More information", url= "https://sites.google.com/hdsb.ca/discordadvertisementbot/home")
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/813464276240564284/56e1793be0b9b313b74ef03a4a154404.png?size=4096")
    embed.add_field(name="Help:", value=f"{d.Prefix}help| Runs this current command", inline=False)
    embed.add_field(name="Up:", value=f"{d.Prefix}up| Checks to see if the bot is online. If the bot is online it will return a message", inline=False)
    embed.add_field(name="Setadmin", value=f"{d.Prefix}setadmin| this command adds the person who sent the message or whoever was pinged in the message as an admin. ADMIN ONLY",
                    inline=False)
    embed.add_field(name="Sendad", value=f"{d.Prefix}sendad| will force send an advertisement. DEV ONLY", inline=False)
    embed.add_field(name="Adchannel", value=f"{d.Prefix}adchannel| Will set the channel the message was sent in as the advertisement channel OR will set the channel the" +
    " user pinged as the ad channel. ADMIN ONLY", inline=False)
    embed.add_field(name="Adfreq", value=f"{d.Prefix}adfreq (int)| This will set how often an advertisement is sent in the server. ADMIN ONLY", inline=False)
    embed.add_field(name="Wallet", value=f"{d.Prefix}wallet| Will tell the user how much money is currently in the servers wallet. ADMIN ONLY", inline=False)
    await channel.send(embed=embed)

@d.bot.command()
@d.client.event
async def on_message(message):
    # checks if message sender was the bot and if so to ignore it
    if message.author == d.client.user:
        return

    print(f"Servers: {d.servers}\nAd ids: {d.ad_ids}\n")
    # checks where the message was sent and adds 1 to the ticker for that server
    for server in d.servers:
        if message.guild.id == server[0]:
            server[1] += 1
            if server[1] % server[3] == 0:
                await sendAd(message)

    # checks if message.content = up and if so to run the up command
    if message.content == str(f"{d.Prefix}up"):
        await message.channel.send("Currently online")

    # checks if message.conent = help and if so to run the help command
    elif message.content == str(f"{d.Prefix}help"):
        channel = d.client.get_channel(message.channel.id)
        await displayhelpembed(channel)

    # checks if message.content starts with setadmin and if so it runs some logic to figure out what the message contains and then to append where required
    elif message.content.startswith(f"{d.Prefix}setadmin"):
        if message.author.id in d.Admins:
            if len(message.content) == len(d.Prefix) + 8:
                if message.author.id in d.Admins:
                    return
                else:
                    d.Admins.append(message.author.id)
                    print(d.Admins)
            else:
                try:
                    id = int(message.content[len(d.Prefix) + 11: len(message.content) - 1])
                    if id in d.Admins:
                        return
                    else:
                        d.Admins.append(id)
                        print(f"Id:{id}\n{d.Admins")
                except ValueError:
                    await message.channel.send("please ping a user")

    # checks if message.content = sendad and if so to forcefully send an ad (for dev purpose's)
    elif message.content == str(f"{d.Prefix}sendad"):
        if message.author.id == 554486518543155212:
            await sendAd(message)
            print("ad sent")
        else:
           await message.channel.send("You are required to be admin for this action")

    # will replace the ad channel with an updated version
    elif message.content.startswith(f"{d.Prefix}adchannel"):
        if message.author.id in d.Admins:
            for server in d.servers:

                if message.guild.id == server[0]:
                    null2 = server[2]
                    server[2] = message.channel.id
                    await message.channel.send(f"Old advert chat:{null2}\nNew advert chat:{server[2]}")

    # will replace the ad frequency 
    elif message.content.startswith(f"{d.Prefix}adfreq"):
        if message.author.id in d.Admins:
            for server in d.servers:
                if message.guild.id == server[0]:
                    try:
                        null1 = server[3]
                        server[3] = int(message.content[len(d.Prefix) + 7: len(message.content)])
                        await message.channel.send(f"Old ad frequency: {null1}\nNew ad frequency: {server[3]}")
                    except(ValueError):
                        await message.channel.send("Please include an int")
    
    # will return the current balance of the wallet
    elif message.content == str(f"{d.Prefix}wallet"):
        if message.author.id in d.Admins:
            for server in d.servers:
                if message.guild.id == server[0]:
                    await message.channel.send(f"Your current balance is: {server[4]}")

# runs the bot token (env var)
d.client.run(os.getenv("var1"))
