import os
import asyncio
from pathlib import Path

import discord
from discord.ext import tasks
from dotenv import load_dotenv

from database.database import get_latest_news
from news.collector import collect_news


# ==========================================
# LOAD ENV
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)

TOKEN = os.getenv("DISCORD_TOKENN")
CHANNEL_ID = os.getenv("DISCORD_CHANNEL")

if not TOKEN:
    raise RuntimeError(
        "DISCORD_TOKEN tidak ditemukan di .env"
    )

if not CHANNEL_ID:
    raise RuntimeError(
        "DISCORD_CHANNEL_ID tidak ditemukan di .env"
    )

CHANNEL_ID = int(CHANNEL_ID)


# ==========================================
# DISCORD
# ==========================================

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

class NewsView(discord.ui.View):

    def __init__(self, link):
        super().__init__(timeout=None)

        self.add_item(
            discord.ui.Button(
                label="📖 Read Article",
                style=discord.ButtonStyle.link,
                url=link
            )
        )


# ==========================================
# SEND NEWS TO DISCORD
# ==========================================

async def send_news(news):

    channel = client.get_channel(CHANNEL_ID)

    if channel is None:

        try:
            channel = await client.fetch_channel(CHANNEL_ID)

        except Exception as error:

            print(
                f"[ERROR] Tidak bisa menemukan channel: {error}"
            )

            return

    source = news["source"]
    title = news["title"]
    link = news["link"]
    category = news["category"]
    summary = news.get("summary", "")
    published = news.get("published", "")
    image_url = news.get("image_url", "")

    # Batasi summary agar Embed tidak terlalu panjang
    if not summary:
        summary = "Tidak ada ringkasan yang tersedia."

    if len(summary) > 1000:
        summary = summary[:997] + "..."

    # Buat Embed
    embed = discord.Embed(
        title=title[:256],
        description=summary,
        url=link
    )

    embed.add_field(
        name="📂 Kategori",
        value=category,
        inline=True
    )

    embed.add_field(
        name="📰 Sumber",
        value=source,
        inline=True
    )

    if published:
        embed.add_field(
            name="📅 Dipublikasikan",
            value=published[:100],
            inline=False
        )


    if image_url:

        embed.set_image(
            url=image_url
        )

    embed.set_footer(
        text="GameDev News Bot • Update otomatis"
    )

    await channel.send(
        embed=embed,
        view=NewsView(link)
    )

    print(
        f"[DISCORD] Berita dikirim: {title}"
    )


# ==========================================
# CHECK NEWS
# ==========================================

@tasks.loop(minutes=5)
async def news_checker():

    print()
    print("==============================")
    print("Memeriksa berita terbaru...")
    print("==============================")

    try:

        # Collector adalah fungsi biasa/synchronous,
        # jadi jalankan di thread agar Discord tidak macet.
        new_articles = await asyncio.to_thread(
            collect_news
        )

        print(
            f"Ditemukan {len(new_articles)} berita baru."
        )

        # Kirim setiap berita baru ke Discord
        for news in new_articles:

            await send_news(news)

            # Jeda sedikit agar tidak mengirim terlalu cepat
            await asyncio.sleep(1)

    except Exception as error:

        print(
            f"[ERROR] News checker: {error}"
        )


@news_checker.before_loop
async def before_news_checker():

    await client.wait_until_ready()


# ==========================================
# BOT READY
# ==========================================

@client.event
async def on_ready():

    print("==============================")
    print("     GAMEDEV NEWS BOT")
    print("==============================")

    print(f"Login sebagai: {client.user}")
    print("Bot berhasil online!")

    print(
        "Auto news checker: setiap 5 menit"
    )

    if not news_checker.is_running():

        news_checker.start()


# ==========================================
# MESSAGE
# ==========================================

@client.event
async def on_message(message):

    # Jangan membalas pesan bot sendiri
    if message.author == client.user:
        return


    # ======================================
    # !PING
    # ======================================

    if message.content.lower() == "!ping":

        await message.channel.send(
            "🏓 Pong! GameDev News Bot aktif."
        )

        return

     # ======================================
        # !TESTNEWS
        # ======================================
    
    if message.content.lower() == "!testnews":
    
            test_news = {
                "source": "GameDev News Test",
                "title": "🧪 Test Automatic News",
                "link": "https://godotengine.org/",
                "published": "Test",
                "category": "TEST",
                "summary": (
                    "Ini adalah berita percobaan untuk memastikan "
                    "bot dapat mengirim informasi ke channel Discord."
                )
            }
    
            await send_news(test_news)
    
            return


    # ======================================
    # !LATEST
    # ======================================

    if message.content.lower() == "!latest":

        news_list = get_latest_news(5)

        if not news_list:

            await message.channel.send(
                "📭 Belum ada berita di database."
            )

            return


        for source, title, link, published, category in news_list:

            embed = discord.Embed(
                title=title[:256],
                description=(
                    f"📰 Berita dari **{source}**"
                ),
                url=link
            )

            embed.add_field(
                name="Kategori",
                value=category,
                inline=True
            )

            embed.add_field(
                name="Sumber",
                value=source,
                inline=True
            )

            embed.set_footer(
                text="GameDev News Bot"
            )

            await message.channel.send(
                embed=embed
            )

        return

   


# ==========================================
# START BOT
# ==========================================

client.run(TOKEN)
