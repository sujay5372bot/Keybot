from pyrogram import Client, filters
from pyrogram.errors import SessionPasswordNeeded
from config import API_ID, API_HASH
from database import add_user

login_state = {}

def setup_login(app):

    @app.on_message(filters.command("login"))
    async def login_start(_, m):
        uid = m.from_user.id
        login_state[uid] = {}
        await m.reply("📞 Send phone number with country code\nExample: +918371054739")

    @app.on_message(filters.text & filters.private & ~filters.regex("^/"))
    async def login_process(_, m):
        uid = m.from_user.id
        if uid not in login_state:
            return

        state = login_state[uid]

        # STEP 1: PHONE
        if "phone" not in state:
            state["phone"] = m.text.strip()
            client = Client(f"sessions/{uid}", API_ID, API_HASH)
            await client.connect()
            sent = await client.send_code(state["phone"])
            state["hash"] = sent.phone_code_hash
            await client.disconnect()

            await m.reply("🔐 Send OTP")
            return

        # STEP 2: OTP
        if "otp" not in state:
            state["otp"] = m.text.strip()
            client = Client(f"sessions/{uid}", API_ID, API_HASH)
            await client.connect()
            try:
                await client.sign_in(
                    phone_number=state["phone"],
                    phone_code=state["otp"],
                    phone_code_hash=state["hash"]
                )
            except SessionPasswordNeeded:
                state["2fa"] = True
                await client.disconnect()
                await m.reply("🔑 Send 2FA password")
                return

            # LOGIN SUCCESS
            await client.disconnect()
            login_state.pop(uid)
            add_user(uid)

            await m.reply("✅ Login successful!\nYou can now use /add_rule")
            return

        # STEP 3: 2FA PASSWORD
        if state.get("2fa"):
            client = Client(f"sessions/{uid}", API_ID, API_HASH)
            await client.connect()
            await client.check_password(m.text.strip())
            await client.disconnect()

            login_state.pop(uid)
            add_user(uid)

            await m.reply("✅ Login successful with 2FA!\nUse /add_rule")
