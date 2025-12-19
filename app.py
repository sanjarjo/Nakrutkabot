# app.py
from fastapi import FastAPI, Request
from bot import create_bot
from telegram import Update

import asyncio
import os

app = FastAPI()
tg_app = create_bot()

# Root route
@app.get("/")
async def root():
    return {"message": "SMM Bot ishlayapti 🚀"}

# Webhook route
@app.post(f"/webhook/{tg_app.bot.token}")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, tg_app.bot)
    await tg_app.process_update(update)
    return {"ok": True}

# Run server with uvicorn: uvicorn app:app --host 0.0.0.0 --port $PORT
