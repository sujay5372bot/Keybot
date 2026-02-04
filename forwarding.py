import asyncio
from pyrogram import Client
from database import get_rules, is_forwarding

clients = {}

async def start_forward(uid, api_id, api_hash):
    if uid in clients:
        return

    client = Client(f"sessions/{uid}", api_id, api_hash)
    await client.start()
    clients[uid] = client

    @client.on_message()
    async def handler(_, m):
        if not is_forwarding(uid):
            return

        rules = get_rules(uid)   # ✅ yahin rehna chahiye

        for s, d, k in rules:
            if m.chat and m.chat.id == s:
                if not k or (m.text and any(x in m.text.lower() for x in k.split(","))):
                    await m.forward(d)
                    await asyncio.sleep(1)

async def stop_forward_client(uid):
    client = clients.get(uid)
    if client:
        await client.stop()
        clients.pop(uid)
