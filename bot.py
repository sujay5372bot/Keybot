import os
import asyncio
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from pyrogram import Client, filters
from config import *
from login import setup_login
from rules import setup_rules
from admin import setup_admin
from forwarding import start_forward, stop_forward_client
from database import start_forward as sf, stop_forward
from expiry_checker import run


# ---------------- HEALTH CHECK SERVER (KOYEB FREE) ----------------

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, format, *args):
        return


def start_health_server():
    port = int(os.getenv("PORT", 8000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()


threading.Thread(target=start_health_server, daemon=True).start()

# ---------------- TELEGRAM BOT ----------------

app = Client("bot", API_ID, API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(_, m):
    await m.reply("🤖 Auto Forward Bot\n/login\n/add_rule\n/start_forwarding")

@app.on_message(filters.command("start_forwarding"))
async def sfwd(_, m):
    uid = m.from_user.id
    sf(uid)
    asyncio.create_task(start_forward(uid, API_ID, API_HASH))
    await m.reply("✅ Forwarding started")

@app.on_message(filters.command("stop_forwarding"))
async def stfwd(_, m):
    uid = m.from_user.id
    stop_forward(uid)
    await stop_forward_client(uid)
    await m.reply("🛑 Forwarding stopped completely")


setup_login(app)
setup_rules(app)
setup_admin(app)

threading.Thread(target=run, daemon=True).start()

app.run()
