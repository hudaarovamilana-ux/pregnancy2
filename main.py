import asyncio
import os

from flask import Flask, abort, request
from aiogram.types import Update

from bot import bot, dp
from database import init_db


app = Flask(__name__)
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")


@app.get("/")
def healthcheck():
    return "OK", 200


@app.post("/api/webhook")
def telegram_webhook():
    if WEBHOOK_SECRET:
        incoming_secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
        if incoming_secret != WEBHOOK_SECRET:
            abort(403)

    data = request.get_json(silent=True)
    if not data:
        abort(400)

    update = Update.model_validate(data, context={"bot": bot})
    init_db()
    asyncio.run(dp.feed_update(bot, update))
    return {"ok": True}, 200

