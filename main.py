import os
from dotenv import load_dotenv
import random

import discord
from discord.ext import commands

import yt_dlp
from discord import FFmpegPCMAudio

load_dotenv()

TOKEN = os.getenv('TOKEN')

# BOT SETUP
intents = discord.Intents.default()
intents.messages = True  # Allow message reception
intents.message_content = True  # Allow message content to be read
intents.guilds = True  # Allow server evnet reception
intents.voice_states = True  # Allow voice channel reception

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='greeting')
async def greeting(ctx):
    responses = [
        f'메리 크리스마스! {ctx.author.mention}! 🎄❤️',
        '12월 25일은 Python의 생일이기도 하다는 걸 알고 있나요?',
        '크리스마스엔 따듯한 커피와 함께 코딩하는 게 최고죠! ☕',
    ]
    await ctx.send(random.choice(responses))

@bot.command(name='play')
async def play(ctx, *, query: str):
    # Join the voice channel
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice_channel = await channel.connect()

        # Extract audio from Youtube video URL with yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'audioquality': 1,
            'outtmpl': 'downloads/%(id)s.%(ext)s',
            'restrictfilenames': True,
            'noplaylist': True,
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Import audio information from Youtube with a discovered URL or query
            info = ydl.extract_info(f'ytsearch:{query}', download=False)
            url = info['entries'][0]['url']  # Get the first video URL

            # Audio Streaming with FFmpeg
            voice_channel.play(FFmpegPCMAudio(url))

            await ctx.send(f'-- SantaChan은 **{query}** 를 연주하기 시작한다 --')

    else:
        await ctx.send(f'{ctx.author.name}님, 음성 채널에 먼저 들어가주세요! 🫠')

@bot.command(name='stop')
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("연주를 멈추고 음성 채널에서 나갈게요!")
    else:
        await ctx.send("엥? 전 지금 아무것도 연주하고 있지 않은데요...")

bot.run(TOKEN)