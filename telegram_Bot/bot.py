import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile
from yt_dlp import YoutubeDL

logging.basicConfig(level=logging.INFO)

# Твой рабочий токен
API_TOKEN ="8937298211:AAGRKMjPqXPfjmmqTEPOIOFIpoS_NNz8coM"

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

    # Проверяем, что нам скинули именно ссылку
    if not url.startswith("http"):
        await message.answer("Пожалуйста, отправь корректную ссылку на видео.")
        return

    status_message = await message.answer("🔄 Начинаю скачивание видео, подожди немного...")

    # Настройки для скачивания (скачиваем видео + аудио в хорошем качестве, но до 50мб для Телеграма)
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': 'video_%(id)s.%(ext)s',
        'max_filesize': 50000000, # ограничение 50 МБ
        'quiet': True
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            # Извлекаем информацию и скачиваем
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # Проверяем расширение (иногда оно может измениться в процессе)
            if not os.path.exists(filename) and os.path.exists(filename.rsplit('.', 1)[0] + '.mp4'):
                filename = filename.rsplit('.', 1)[0] + '.mp4'

        await status_message.edit_text("🚀 Видео скачано на сервер! Отправляю тебе в чат...")

        # Отправляем файл пользователю
        video_file = FSInputFile(filename)
        await message.answer_video(video=video_file, caption=info.get('title', 'Ваше видео'))
        
        # Удаляем файл с компьютера, чтобы не занимать место
        os.remove(filename)
        await status_message.delete()

    except Exception as e:
        logging.error(e)
        await status_message.edit_text(f"❌ Произошла ошибка при скачивании. Возможно, видео слишком длинное или приватное.")
        # Если файл остался, чистим за собой
        if 'filename' in locals() and os.path.exists(filename):
            os.remove(filename)

async def main():
    print("Бот-скачиватель запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())