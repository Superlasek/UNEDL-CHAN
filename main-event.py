import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord import Activity, ActivityType
#from dotenv import load_dotenv
import urllib.request
import json
import random
import asyncio
import math
import wikipedia

# -------- CARGADO DEL BOT

#TOKEN = ''

load_dotenv() # Carga el archivo env
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print('Cliente 2 listo :)')

def wiki_summary(arg):
    definition = wikipedia.summary(arg, sentences=3, chars=100,
    auto_suggest=True, redirect=True)
    return definition

wikipedia.set_lang("es")

# -------- EVENTOS

@client.event
async def on_message(mensaje):
    words = mensaje.content.split()
    if words[0].lower() == "pedia":
        important_words = words[1:]
        embed = discord.Embed(title="UNEDL-PEDIA (￣▽￣)", description=wiki_summary(important_words), color=discord.Color.green())
        await mensaje.channel.send(embed = embed)
    if mensaje.content.find('xd')!=-1:
        await mensaje.channel.send('XD')
    if mensaje.content.find(':v')!=-1:
        await mensaje.channel.send('Baia baia, un grasoso')
    if mensaje.content.find('puto')!=-1:
        await mensaje.channel.send('hey {0.author.mention} que grosero'.format(mensaje))
    if mensaje.content.find('pendejo')!=-1:
        await mensaje.channel.send('hey {0.author.mention} que grosero'.format(mensaje))
    if mensaje.content.find('puta')!=-1:
        await mensaje.channel.send('hey {0.author.mention} que grosero'.format(mensaje))
    if mensaje.content.find('nigga')!=-1:
        await mensaje.channel.send('hey {0.author.mention} que grosero'.format(mensaje))
    if mensaje.content.find('maestra tovar')!=-1:
        await mensaje.channel.send('https://meet.google.com/xrd-cohi-eey')


# --------

client.run(TOKEN) # Run del bot
