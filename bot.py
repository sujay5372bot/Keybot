import asyncio, threading
from pyrogram import Client, filters
from config import *
from login import setup_login
from rules import setup_rules
from admin import setup_admin
from forwarding import start_forward
from database import start_forward as sf, stop_forward
from expiry_checker import run

app = Client("bot", API_ID, API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(_, m):
    await m.reply("🤖 Auto Forward Bot\n/login\n/add_rule\n/start_forwarding")

@app.on_message(filters.command("start_forwarding"))
async def sfwd(_, m):
    sf(m.from_user.id)
    asyncio.create_task(start_forward(m.from_user.id, API_ID, API_HASH))
    await m.reply("✅ Forwarding started")

@app.on_message(filters.command("stop_forwarding"))
async def stfwd(_, m):
    stop_forward(m.from_user.id)
    await m.reply("🛑 Forwarding stopped")

setup_login(app)
setup_rules(app)
setup_admin(app)

threading.Thread(target=run, daemon=True).start()

app.run()
