from pyrogram import filters
from database import add_rule, get_rules, is_premium

pending = {}

def setup_rules(app):

    @app.on_message(filters.command("add_rule"))
    async def start(_, m):
        uid = m.from_user.id
        if not is_premium(uid) and len(get_rules(uid)) >= 2:
            await m.reply("❌ Free limit reached. Buy premium.")
            return
        pending[uid] = {}
        await m.reply("📥 Send SOURCE chat ID")

    @app.on_message(filters.text & filters.private & ~filters.regex("^/"))
    async def process(_, m):
        uid = m.from_user.id
        if uid not in pending:
            return
        data = pending[uid]

        if "s" not in data:
            data["s"] = int(m.text)
            await m.reply("📤 Send DESTINATION chat ID")
            return

        if "d" not in data:
            data["d"] = int(m.text)
            await m.reply("🔎 Send keywords or `skip`")
            return

        k = "" if m.text.lower()=="skip" else m.text.lower()
        add_rule(uid, data["s"], data["d"], k)
        pending.pop(uid)
        await m.reply("✅ Rule added")
