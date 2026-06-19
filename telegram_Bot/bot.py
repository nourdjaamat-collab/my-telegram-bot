import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile
from yt_dlp import YoutubeDL

logging.basicConfig(level=logging.INFO)

# Твой токен
API_TOKEN = "8937298211:AAGRKMjPqXPFjmmqTEPOIOFIpoS_NNz8coM"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    await message.answer(
        "Привет! Я бот для скачивания видео с YouTube.\n\n"
        "Просто отправь мне ссылку на видео, и я пришлю тебе его файлом!"
    )

@dp.message()
async def download_video(message: types.Message):
    url = message.text
    if "youtube.com" in url or "youtu.be" in url:
        await message.answer("Начинаю скачивание видео, подожди немного...")
        try:
            ydl_opts = {
                'outtmpl': 'video.mp4',
                'format': 'best[ext=mp4]/best',
            }
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            video_file = FSInputFile("video.mp4")
            await message.answer_video(video_file, caption="Вот твое видео!")
            
            if os.path.exists("video.mp4"):
                os.remove("video.mp4")
        except Exception as e:
            await message.answer(f"Произошла ошибка при скачивании: {e}")
    else:
        await message.answer("Пожалуйста, отправь корректную ссылку на YouTube видео.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
