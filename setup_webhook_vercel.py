import asyncio
import os

from aiogram import Bot


TOKEN = os.getenv("BOT_TOKEN")
VERCEL_URL = os.getenv("VERCEL_URL")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

if not VERCEL_URL:
    raise RuntimeError("VERCEL_URL is not set, expected format: https://<project>.vercel.app")


async def main():
    bot = Bot(token=TOKEN)
    webhook_url = f"{VERCEL_URL.rstrip('/')}/api/webhook"

    await bot.set_webhook(
        url=webhook_url,
        secret_token=WEBHOOK_SECRET if WEBHOOK_SECRET else None,
        drop_pending_updates=False,
    )
    info = await bot.get_webhook_info()
    print(f"Webhook URL: {info.url}")
    print(f"Pending updates: {info.pending_update_count}")
    await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
