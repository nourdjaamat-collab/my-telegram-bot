import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile
from yt_dlp import YoutubeDL

logging.basicConfig(level=logging.INFO)

# Твой рабочий токен (я взял его с твоего скриншота)
API_TOKEN = "8937298211:AAGRKMjPqXPFjmmqTEPOIOFIpoS_NNz8coM"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    await message.answer(
        "Привет! Я бот для скачивания видео с YouTube.\n\n"
        "Просто отправь мне ссылку на видео, и я пришлю тебе его файлом!"
    )

# Ниже должен идти твой остальной код для скачивания видео...
