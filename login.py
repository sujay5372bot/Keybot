from pyrogram import Client, filters
from pyrogram.errors import SessionPasswordNeeded
from config import API_ID, API_HASH
from database import set_logged_in

pending_login = {}

def setup_login(app):

    @app.on_message(filters.command("login"))
    async def login(_, message):
        user_id = message.from_user.id
        pending_login[user_id] = {}
        await message.reply_text("📞 Apna phone number country code ke sath bhejo\nExample: +919876543210")

    @app.on_message(filters.text & filters.private)
    async def process_login(_, message):
        user_id = message.from_user.id

        if user_id not in pending_login:
            return

        data = pending_login[user_id]

        # Step 1: Phone
        if "phone" not in data:
            data["phone"] = message.text
            client = Client(
                f"sessions/{user_id}",
                api_id=API_ID,
                api_hash=API_HASH
            )
            await client.connect()
            sent = await client.send_code(data["phone"])
            data["hash"] = sent.phone_code_hash
            await client.disconnect()
            await message.reply_text("🔐 OTP bhejo")
            return

        # Step 2: OTP
        if "otp" not in data:
            data["otp"] = message.text
            client = Client(
                f"sessions/{user_id}",
                api_id=API_ID,
                api_hash=API_HASH
            )
            await client.connect()
            try:
                await client.sign_in(
                    phone_number=data["phone"],
                    phone_code=data["otp"],
                    phone_code_hash=data["hash"]
                )
            except SessionPasswordNeeded:
                await message.reply_text("🔑 2-step password bhejo")
                data["2fa"] = True
                await client.disconnect()
                return

            set_logged_in(user_id)
            await client.disconnect()
            pending_login.pop(user_id)
            await message.reply_text("✅ Login successful! Ab /add_rule use karo")
            return

        # Step 3: 2FA
        if data.get("2fa"):
            client = Client(
                f"sessions/{user_id}",
                api_id=API_ID,
                api_hash=API_HASH
            )
            await client.connect()
            await client.check_password(message.text)
            set_logged_in(user_id)
            await client.disconnect()
            pending_login.pop(user_id)
            await message.reply_text("✅ Login successful with 2FA!")
