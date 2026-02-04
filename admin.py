from pyrogram import filters
from config import ADMIN_ID
from database import stats, set_premium

def setup_admin(app):

    @app.on_message(filters.command("admin") & filters.user(ADMIN_ID))
    async def admin(_, m):
        s = stats()
        await m.reply(f"👥 {s['users']}\n💎 {s['premium']}\n🚀 {s['forwarding']}")

    @app.on_message(filters.command("add_premium") & filters.user(ADMIN_ID))
    async def addp(_, m):
        uid = int(m.text.split()[1])
        set_premium(uid, 30)
        await m.reply("✅ Premium added")
