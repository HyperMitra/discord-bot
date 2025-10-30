import os
import asyncio
import logging
from typing import Dict, Optional, List

import requests
from bs4 import BeautifulSoup

import aiohttp
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


CHANNEL_ID = 1153263160556531762 


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "mistralai/mistral-7b-instruct"


USER_AGENT = "Mozilla/5.0 (DiscordBot; subreddit watcher by @you)"
BROWSER_HEADERS = {"User-Agent": USER_AGENT}


session: Optional[aiohttp.ClientSession] = None


@bot.command()
async def ping(ctx): await ctx.send("Boop!")

@bot.command()
async def copper(ctx): await ctx.send("Ea nasir!")

@bot.command()
async def sus(ctx): await ctx.send("your a sussy baka and you know that!")

@bot.command()
async def name(ctx): await ctx.send("hyperion!")

@bot.command()
async def Language(ctx):
    await ctx.send("Beginner's Latin Book: https://archive.org/details/beginnerslatinb01collgoog/page/n48/mode/2up?view=theater")

@bot.command()
async def hf(ctx): await ctx.send("Click here to go the Hypixel Forums: https://hypixel.net/")

@bot.command()
async def Latin(ctx):
    await ctx.send("Latin Dictionary Online: https://web.archive.org/web/20231211013956/https://personal.math.ubc.ca/~cass/frivs/latin/latin-dict-full.html")

@bot.command()
async def t(ctx): await ctx.send("https://docs.python.org/3.13/tutorial/")


cuneiform_map = {
    "a":"𒀀","b":"𒁀","c":"𒅝","d":"𒁲","e":"𒂊","f":"𒈿","g":"𒈀","h":"𒈩","i":"𒈿",
    "j":"𐥎","k":"𒋒","l":"𒉻","m":"𒊬","n":"𒋁","o":"Ω","p":"𒁉","q":"𐥒","r":"𒊑",
    "s":"𒊓","t":"𒌾","u":"𒌋","v":"𒇙","w":"𒈿","x":"X","y":"𒇆","z":"ξ"
}
def translate_to_cuneiform(text): return ''.join(cuneiform_map.get(ch, ch) for ch in text.lower())
@bot.command()
async def cuneiform(ctx, *, text): await ctx.send(translate_to_cuneiform(text))

cipherB_map = {
    "a":"B","b":"V","c":"G","d":"Q","e":"C","f":"E","g":"A","h":"Z","i":"N","j":"O",
    "k":"M","l":"X","m":"R","n":"L","o":"P","p":"J","q":"U","r":"H","s":"K","t":"F",
    "u":"W","v":"I","w":"D","x":"X","y":"T","z":"Y"
}
def translate_to_cipherB(text): return ''.join(cipherB_map.get(ch, ch) for ch in text.lower())
@bot.command()
async def cipherB(ctx, *, text): await ctx.send(translate_to_cipherB(text))


@bot.command()
async def ask(ctx, *, question):
    await ctx.typing()
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://mydiscordbot.local",
            "X-Title": "Discord Bot Example",
        }
        data = {"model": OPENROUTER_MODEL, "messages": [{"role": "user", "content": question}]}
        resp = requests.post(OPENROUTER_BASE_URL, headers=headers, json=data, timeout=30)
        resp.raise_for_status()
        result = resp.json()
        message = result["choices"][0]["message"]["content"]
        await ctx.send(message[:1997] + "..." if len(message) > 2000 else message)
    except Exception as e:
        await ctx.send(f"Error: {e}")



    


@bot.event
async def on_ready():
    global session
    logging.info(f"✅ Logged in as {bot.user}")
    session = aiohttp.ClientSession()


@bot.event
async def on_disconnect():
    if session and not session.closed:
        await session.close()


bot.run(TOKEN)




