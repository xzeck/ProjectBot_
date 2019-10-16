from __future__ import unicode_literals
from discord.ext import commands

import discord  # discord API
import youtube_dl  # for downloading the videos
import asyncio  # for invoking commands asynchronously
import os  # for finding the path
import json
import urllib

# load opus if not already loaded
if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')

# Bot Token DO NOT SHARE
TOKEN = "<insert-bot-token-here>"
# Voice Channel ID DO NOT SHARE
ID = "<insert-voice-channel-ID>"
# Prefix by which bot commands are to be given
PREFIX = ("!", "?", "|")
# API link
API = 'https://api.openweathermap.org/data/2.5'
# API key
openweatherkey = '<insert-open-weather-key>'
# to do queue
todo = {}

# playlist queue
playlist = []

# Initializing bot with the given prefix
client = commands.Bot(command_prefix=PREFIX)


# Connect to the text channel and join the voice channel
@client.event
async def on_ready():
    print("logging in")
    # channel = client.get_channel(ID)
    # await client.join_voice_channel(channel)
    print("Bot Should've joined the voice channel")
    if not os.path.exists('cache/'):
        os.mkdir('cache/')


# Download the song
def download_song(link):
    link = str(link)  # converting the link from an object to a string
    # print(link)  # for debugging purposes

    # download options
    ydl_opts = {

        # audio extraction parameters
        # should extract it in AAC codec and at 68kbps
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            'preferredquality': '68',

        }],
        # default_searches youtube for video links
        'default_search': 'ytsearch',
        'foretitle': True,
        'foreurl': True,
        # output template sets the destination for downloads and the format in which it would be named
        'outtmpl': 'cache/%(title)s.%(ext)s',

    }

    # main download block
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        # extracting the metadata from the youtube video
        info_dict = ydl.extract_info(link, download=False)
        # extracting the title from the metadata
        # title = info_dict.get('title', None)

        # sprint(info_dict)
        title = info_dict.get('entries', None)
        for i in title:
            title = i.get('title')
            link = i.get('webpage_url', None)

        title = title.replace('|', "_")
        title = title.replace('"', '\'')

        # checking if the file exists in cache
        print('link' + str(link))
        if not os.path.exists('cache/' + title + '.m4a'):
            ydl.download([link])  # download if file doesn't exist in cache
        else:
            print("pulling from cache")  # pull from cache

        return title  # return the title


# saying this is a client command
@client.command(
    name='play',  # Name by which the command will be triggered/invoked in discord
    description='Plays Music',  # description
    brief='Plays Music syntax : !play <youtube-link>',
    pass_context=True,  # used to pass context, as in the details about the sent message
    aliases=['music']  # Aliases so that the command can be triggered/invoked by the alias as well
)
async def play(context):
    user = context.message.author  # get the author of the sent message
    voice_channel = user.voice.voice_channel  # get the voice channel in which the author is in
    print(voice_channel)
    channel = None
    print('Discord Server name')
    print(client.is_voice_connected(voice_channel))

    if not client.is_voice_connected(voice_channel):
        vc = await client.join_voice_channel(voice_channel)

    if voice_channel is not None:  # Only if the user is in a voice channel

        # print(type(vc))
        # grab user's voice channel
        channel = voice_channel.name  # get channel name
        link = context.message.content.split("!play")  # split the sent message content by " "
        link = link[1]  # split content is stored in a list, get the second element of the list which is the link
        print(link)
        playlist.append(link)

        title = download_song(playlist[0])  # get the title and download the song
        await client.say(
            'Playing : {} requested by {}'.format(str(title), user.mention))  # send a message saying the
        # currently playing song and who requested
        # join channel
        completelink = 'cache/' + title + '.m4a'  # generate the local file link/path
        # create a fmmpeg player with the local file
        player = vc.create_ffmpeg_player(completelink, after=lambda: print('done'))
        # print(type(player))  # for debugging
        # start the player
        playlist.pop()
        player.start()
        # wait till the player is done playing
        while not player.is_done():
            await asyncio.sleep(1)

        # stop the player and disconnect from the channel
        player.stop()
        # await vc.disconnect()

    else:
        await client.say('{} is not in a voice channel.'.format(user.mention))  # display if the user is not in any
        # channel


@client.command(
    name='weather',
    description='Gets the weather details',
    brief='Gets the weather details syntax !weather <NAME OF CITY>',
    pass_context=True,
    aliases=['temperature'],

)
async def weather(context):
    # http://api.openweathermap.org/data/2.5/weather?q=mumbai&appid=4b205f43acf4015aee44b3f1bb94cd7a

    message = context.message.content  # get the user messsage
    message = message.split(" ")  # split by space
    count = len(message)

    if count is 3:
        city = '{} {}'.format(message[1], message[2])
    else:
        city = '{}'.format(message[1])

    print(city)  # for debugging

    # generating the weatherapi access link
    completelink = API + '/weather?q=' + city + '&appid=' + openweatherkey + '&units=metric'
    # get response from web
    response = urllib.request.urlopen(completelink)
    # load the json response to data
    data = json.load(response)
    print(data)  # for debugging

    temp = data.get('main').get('temp')  # data is in the form of a dictionary, get 'temp' element from 'main'

    await client.say(
        '{} Current weather in {} is {}C'.format(context.message.author.mention, city, temp))  # formatting bot message


@client.command(
    name='forecast',
    description='Gets the forecast for the following days',
    brief='Gets the forecast of weather upto 16 days syntax : !forecast <NAME OF CITY> <NO OF DAYS>',
    pass_context=True,

)
async def forecast(context):
    message = context.message.content  # message
    message = message + ' 5'  # weird workaround to solve
    message = message.split(" ")

    count = len(message)

    if count is 5:
        city = '{} {}'.format(message[1], message[2])
        days = int(eval(message[3]))
    else:
        city = message[1]
        days = int(eval(message[2]))  # eval() so that if a neegative number of days is entered it can still evaluate to
    # correct in the lines below, int(message[2]) doesn't eval signed integers

    """
    How weird work around works: 
    
    If the message is '!forecast Mumbai' 
    then add 5 as a default parameter for the required number of days the forecast is requested for. 
    
    if the message is '!forecast Mumbai 10' 
    then add 5 as a default parameter, since the program only checks till message[2] the 5 will not be read
    and 10 will be passed as the required number of days the forecast is requested for.
    """

    if days > 16:  # check if days is greater than 16, because API can only pull forecast for 16 days
        days = 16  # if entered number of days is more than 16, set it to 16

    if days < 0:  # check if entered number of days is less than 0
        days = 5  # if entered number of days is less than 0, set it to 5

    print(city)  # for debugging

    # generating api request link
    completelink = API + '/forecast?q=' + city + '&appid=' + openweatherkey + '&units=metric'
    response = urllib.request.urlopen(completelink)  # get the response
    data = json.load(response)  # load the json into data

    temp = data.get('list')  # from the dictionary get the list named 'list'

    forecast_temp = []  # list to contain the json data of forecast temp
    for i in range(0, days):  # go from 0 to given number of days by user
        t = temp[i]  # get the 'i'th element which is a dictionary
        # from the recieved 'i'th element which is a dictionary, get the key main and from main get the key 'temp'
        t = t.get('main').get('temp')
        # append value to the list
        forecast_temp.append(t)

    weatherforecast = ""  # initializing weatherforecast which will contain the whole message the bot will send
    # print(type(forecast_temp))  # for debugging

    # itterate through the forecast_temp list and get each item and temporarily store it in item
    # 'i' will save the day count and item will hold the temperature, enumerate through the forecast_temp list
    for (i, item) in enumerate(forecast_temp):
        # formatting bot message
        weatherforecast = weatherforecast + '\nTemperature for Day {} is {} C\n'.format(i + 1, item)

    # mentioning author and send the forecast
    await client.say('{} The forecast is :'.format(context.message.author.mention) + weatherforecast)


@client.command(
    name='exch',
    description='Currency Exchange rate',
    brief='Currency Exchange Rate. Syntax : !exch <From> <To> <Amount>',
    pass_context=True,
)
async def event(context):
    message = context.message.content
    # "http://free.currencyconverterapi.com/api/v5/convert?q=" + CurrencyFromConvert + "_" + CurrencyToConvert +
    # "&compact=y"
    message = message.split(" ")

    try:
        from_curr = message[1]
        to_curr = message[2]
        amount = message[3]

    except:
        await client.say('{} please use the proper syntax !exch <From> <To> <Amount>'.format(
            context.message.author.mention))

    if from_curr is None or to_curr is None or amount is None:
        await client.say('{} please use the proper syntax !exch <From> <To> <Amount>'.format(
            context.message.author.mention))
    else:
        completelink = 'http://free.currencyconverterapi.com/api/v5/convert?q={}_{}&compact=y'.format(from_curr,
                                                                                                      to_curr)
        response = urllib.request.urlopen(completelink)
        data = json.load(response)
        exrat = data.get('{}_{}'.format(from_curr, to_curr))
        exrat = exrat.get('val')
        exrat = float(exrat)
        amount = amount
        amount = float(amount)
        amount = amount * -1
        convamount = float(amount * exrat)
        print('String')
        print(type(convamount))
        await client.say('{} {} from {} to {} is : {}'.format(context.message.author.mention, amount, from_curr,
                                                              to_curr, convamount))


client.run(TOKEN)  # start/run the bot by passing the token
