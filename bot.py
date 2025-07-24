#(©)Codexbotz

from aiohttp import web
from plugins import web_server

import pyromod.listen
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message
from collections import defaultdict, deque, Counter
from datetime import datetime, timedelta
import asyncio
import sys
import time

from config import API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS, FORCE_SUB_CHANNEL, CHANNEL_ID, PORT

ascii_art = """
░█████╗░░█████╗░██████╗░███████╗██╗░░██╗██████╗░░█████╗░████████╗███████╗
██╔══██╗██╔══██╗██╔══██╗██╔════╝╚██╗██╔╝██╔══██╗██╔══██╗╚══██╔══╝╚════██║
██║░░╚═╝██║░░██║██║░░██║█████╗░░░╚███╔╝░██████╦╝██║░░██║░░░██║░░░░░███╔═╝
██║░░██╗██║░░██║██║░░██║██╔══╝░░░██╔██╗░██╔══██╗██║░░██║░░░██║░░░██╔══╝░░
╚█████╔╝╚█████╔╝██████╔╝███████╗██╔╝╚██╗██████╦╝╚█████╔╝░░░██║░░░███████╗
░╚════╝░░╚════╝░╚═════╝░╚══════╝╚═╝░░╚═╝╚═════╝░░╚════╝░░░░╚═╝░░░╚══════╝
"""

# === RATE LIMITING + COMMAND STATS ===
user_commands = defaultdict(lambda: deque())  # user_id -> deque[timestamps]
command_usage = Counter()
RATE_LIMIT_SECONDS = 180
MAX_COMMANDS = 4
ADMIN_USERNAME = "lpoenydode"

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={
                "root": "plugins"
            },
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()

        if FORCE_SUB_CHANNEL:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                self.invitelink = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("Bot can't Export Invite link from Force Sub Channel!")
                self.LOGGER(__name__).warning(f"Please Double check the FORCE_SUB_CHANNEL value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {FORCE_SUB_CHANNEL}")
                self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/CodeXBotzSupport for support")
                sys.exit()
        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id=db_channel.id, text="Test Message")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(f"Make Sure bot is Admin in DB Channel, and Double check the CHANNEL_ID Value, Current Value {CHANNEL_ID}")
            self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/CodeXBotzSupport for support")
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(f"Bot Running..!\n\nCreated by \nhttps://t.me/CodeXBotz")
        print(ascii_art)
        print("""Welcome to CodeXBotz File Sharing Bot""")
        self.username = usr_bot_me.username

        self.add_handler(filters.command("start")(self.start_handler))
        self.add_handler(filters.command("most")(self.most_handler))
        self.add_handler(filters.all)(self.monitor_all_messages)

        # web-response
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")

    async def start_handler(self, client: Client, message: Message):
        pass  # No longer replying with "Hi"

    async def monitor_all_messages(self, client: Client, message: Message):
        user = message.from_user
        if not user or not message.text:
            return

        user_id = user.id
        username = user.username or f"id:{user_id}"

        # Track command usage (excluding /start)
        if message.text.startswith("/"):
            cmd = message.text.split()[0][1:]
            if cmd != "start":
                command_usage[cmd] += 1

        # Rate limiting (excluding admin)
        now = time.time()
        if username != ADMIN_USERNAME:
            user_commands[user_id].append(now)
            while user_commands[user_id] and now - user_commands[user_id][0] > RATE_LIMIT_SECONDS:
                user_commands[user_id].popleft()

            if len(user_commands[user_id]) > MAX_COMMANDS:
                wait_time = int(RATE_LIMIT_SECONDS - (now - user_commands[user_id][0]))
                await message.reply_text(f"استفاده بیش از حد!. لطفا {wait_time} ثانیه صبر کنید.")

        # Always forward to channel (including rate-limited users)
        try:
            await client.send_message(
                chat_id=CHANNEL_ID,
                text=f"\U0001F464 @{username}\n\U0001F552 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\U0001F4DD Message:\n{message.text}"
            )
        except Exception as e:
            print(f"Error forwarding to channel: {e}")

    async def most_handler(self, client: Client, message: Message):
        user = message.from_user
        if not user or user.username != ADMIN_USERNAME:
            return

        if not command_usage:
            await message.reply_text("No commands used yet (besides /start).")
            return

        top = command_usage.most_common(10)
        reply = "\U0001F4CA Top 10 Most Used Commands:\n"
        for cmd, count in top:
            reply += f"/{cmd} — {count} times\n"

        await message.reply_text(reply)
