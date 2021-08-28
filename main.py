import os
from dotenv import load_dotenv
from re import search
import discord
from discord import embeds
from discord.colour import Colour
from discord.ext import commands
#from dotenv import load_dotenv
import urllib.request
import json
import random
import asyncio
import math
import datetime
import re
import youtube_dl
from urllib import parse,request
from discord.ext.commands import errors
from discord.utils import get

from discord.ext.commands.core import guild_only

# -------- CARGADO DEL BOT

#TOKEN = ''

load_dotenv() # Carga el archivo env
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

bot = commands.Bot(command_prefix='.uc ', case_insensitive=True) #Prefijo del bot

@bot.event
async def on_ready():
    print('Cliente listo :)')


# -------- COMANDOS
async def background_loop():
    await client.wait_until_ready()
    while not client.is_closed:
        channel = client.get_channel("497205929759211541")
        messages = ["Hola!", "¿Como te encuentras Oni-chan?~", "uwu"]
        await client.send_message(channel, random.choice(messages))
        await asyncio.sleep(10)

@bot.command(name='op')
async def op(ctx, num1, signo, num2):
    if signo == '+':
        response = int(num1) + int(num2)
        await ctx.send(response)
    elif signo == '-':
        response = int(num1) - int(num2)
        await ctx.send(response)
    elif signo == '*':
        response = int(num1) * int(num2)
        await ctx.send(response)
    elif signo == '/':
        try:
            response = int(num1) / int(num2)
            await ctx.send(response)
        except:
            await ctx.send('No se puede dividir entre 0 \nBaka... (￣_￣|||)')
    elif signo == '^':
        response = pow(int(num1), int(num2))
        await ctx.send(response)
    elif signo == '√':
        response = math.sqrt(int(num1))
        await ctx.send(response)

@bot.command()
async def yt(ctx, *,search):
    query_string = parse.urlencode({'search_query': search})
    html_content = request.urlopen('http://www.youtube.com/results?' + query_string)
    search_results = re.findall(r"watch\?v=(\S{11})", html_content.read().decode())
    #print(search_results)
    response = ('https://www.youtube.com/watch?v=' + search_results[0])
    await ctx.send(response)

@bot.command()
async def ayuda(ctx):
    embed = discord.Embed(title="Ayuda (づ￣ 3￣)づ", description="Informacion de los Comandos\nUtilizar con `.uc comandoaqui`\nEjemplo: `.uc op 2 + 2`", color=discord.Color.green())
    embed.add_field(name="Operaciones 🧮", value="`op`\nSuma\nResta\nMultiplicacion\nDivision\nPotencia")
    embed.add_field(name="Juegos 🎮", value="`Ping`\n`Sabia`")
    embed.add_field(name="Saludos 🖐", value="`Hola`")
    embed.add_field(name="Servidor 💾", value="`Info`\n`Groserias`\n`Borrar`")
    embed.add_field(name="Voz 🎤", value="`Unir`\n`Salir`\n`Play`")
    await ctx.send(embed=embed)

    #embed = discord.Embed(
    #    colour = discord.Colour.green()
    #)
    #embed.set_author(name='Ayuda')
    #embed.add_field(name='.uc ping', value='Pong uwu', incline=False)

@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('Pong （￣︶￣)🏓')
    messages = ["¡Te gane! (≧∀≦)", "Perdí... (´。＿。｀)"]
    await ctx.send(random.choice(messages))

@bot.command(name='sabia') #Parte Favorita de Paul
async def sabia(ctx, messages):
    await ctx.send('🔮 La Loli Sabia dice:')
    messages = ["Tal vez", "Definitivamente Si", "Definitivamente No", "Puede Ser"]
    await ctx.send(random.choice(messages))

@bot.command(name='borrar')
async def borrar(ctx, amount=10):
    await ctx.channel.purge(limit=amount)

@bot.command()
async def hola(ctx):
    await ctx.send('Buenas Oni-chan (✿◡‿◡)')


# -------- CONEXIÓN BOT A CHAT VOZ}
# -----------------Entrada
@bot.command(pass_context=True)
async def unir(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    await channel.connect()
    await ctx.send(f"Estoy en {channel}")

# -----------------Salida
@bot.command(pass_context=True)
async def salir(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    await voice.disconnect()
    await ctx.send(f"Salí de {channel}")

# -----------------Reproducir
@bot.command(pass_context=True)
async def play(ctx, url: str):
    song_there = os.path.isfile("cancion.mp3")
    try:
        if song_there:
            os.remove("cancion.mp3")
            print("Se removio la canción")
    except PermissionError:
        print("Se trato de remover la canción pero esta activo")
        await ctx.send("ERROR: Reproduciendo canción.")
        return

    await ctx.send("Listo")

    voice = get (bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Descargando audio\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Archivo renombrado: {file}\n")
            os.rename(file, "cancion.mp3")

    voice.play(discord.FFmpegPCMAudio("cancion.mp3"), after=lambda e: print(f"{name} ha finalizado la reproducción"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 1

    nname = name.rsplit("-", 2)
    await ctx.send(f"Reproduciendo: {nname[0]}")
    print("Reproduciendo audio")

@bot.command()
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="Información breve del servidor. ", timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
    embed.add_field(name="Servidor creado el", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Dueño servidor", value=f"{ctx.guild.owner}")
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    # embed.set_thumbnail(url=f"{ctx.guild.icon}")
    embed.set_thumbnail(url= ctx.guild.icon_url);

    await ctx.send(embed=embed)

bot.loop.create_task(background_loop())

bot.run(TOKEN) # Run del bot
