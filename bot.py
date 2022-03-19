import platform
import lyricsgenius
import discord
import os

from discord.ext import commands
from discord import Spotify
from dotenv import load_dotenv
from numpy import true_divide

load_dotenv()

print(platform.python_version())

discordToken=os.getenv("DISCORD_TOKEN")
geniusToken=os.getenv("GENIUS_TOKEN")

intents = discord.Intents.all()
client = discord.Client(intents = intents)
genius = lyricsgenius.Genius(geniusToken)

@client.event
async def on_ready():
  print('Lyric Bot is logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  text=message.content



  # $lyrics command for lyrics of specified song using Genius
  if text.startswith('$lyrics'):
    if text.strip()=='$lyrics':
      await message.channel.send('Lyrics for which song? \n (ex. "$lyrics Oh Canada")')
    else:
      combinedLyrics = []
      text=text.replace("$lyrics", "")
      await geniusSearch(text, message)
  


  # $song command for Spotify embedded URL of currently played song
  if text.startswith('$current song'):
    user = message.author
    noSpotify = True
    for activity in user.activities:
      if isinstance(activity, discord.Spotify):
        noSpotify = False
        await message.channel.send(f'https://open.spotify.com/track/{activity.track_id}')
    if(noSpotify):
      await message.channel.send(f'{user.name} is not listening to Spotify currently.')



  # $current lyrics command for lyrics of currently played Spotify song from Genius 
  if text.startswith('$current lyrics'):
    user = message.author
    noSpotify = True
    for activity in user.activities:
      if isinstance(activity, discord.Spotify):
        noSpotify = False
        searchString = activity.title+" "+activity.artist
        await message.channel.send(f'https://open.spotify.com/track/{activity.track_id}')
        await geniusSearch(searchString, message)
        break
    if(noSpotify):
      await message.channel.send(f'{user.name} is not listening to Spotify currently.')




#Reusable function for lyrics search process from Genius
async def geniusSearch(text, message):

  try:
    song = genius.search_song(text)
    print(song.lyrics)
    lyricsList = song.lyrics.split('\n')
    n = len(lyricsList)
    print(n)
    x = 0
    while x<n:
      toPrint=""
      for i in range(15):
        if(x==n):
          break
        toPrint=toPrint+"\n"+lyricsList[x]
        x=x+1
      if(toPrint != ""):
        await message.channel.send(toPrint)

  except:
    print("Fetch lyrics failed")
    await message.channel.send('Sorry, couldn''t find lyrics for that song')

  return



client.run(discordToken) 