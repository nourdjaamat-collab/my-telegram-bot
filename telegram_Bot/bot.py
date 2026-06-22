import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from yt_dlp import YoutubeDL

logging.basicConfig(level=logging.INFO)

# Берем токен из настроек Environment, которые мы внесли на Render
API_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = -1004426248134  # ID твоего канала
CHANNEL_URL = "https://t.me/savevideohub"  # Ссылка на твой канал

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Функция для проверки, подписан ли пользователь на канал 
async def check_subscription(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        if member.status in ["creator", "administrator", "member"]:
            return True
        return False
    except Exception as e:
        logging.error(f"Ошибка проверки подписки: {e}")
        return True

@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    await message.answer(
        "Привет! Я бот для скачивания видео с YouTube.\n\n"
        "Чтобы получить возможность скачивать видео, вам необходимо подписаться на наш официальный канал!"
    )

@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    url = message.text

    # Сначала проверяем подписку пользователя
    is_subscribed = await check_subscription(user_id)

    if not is_subscribed:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="👉 ПОДПИСАТЬСЯ НА КАНАЛ", url=CHANNEL_URL)]
        ])
        await message.answer(
            "⚠️ Доступ заблокирован!\n\n"
            "Для использования этого бота и скачивания видео, вам нужно обязательно подписаться на наш канал. "
            "После подписки просто отправьте ссылку на видео ещё раз!",
            reply_markup=keyboard
        )
        return

    # Если подписан, обрабатываем ссылку на YouTube
    if "youtube.com" in url or "youtu.be" in url:
        await message.answer("🔄 Начинаю скачивание видео, подождите немного...")
        try:
            ydl_opts = {
                'outtmpl': f'video_{user_id}.mp4',
                'format': 'best[ext=mp4]/best',
                'cookiefile': os.path.join(os.path.dirname(__file__), 'cookies.txt'),м
                'nocheckcertificate': True,
                'ignoreerrors': False,
                'logtostderr': False,
                'quiet': True,
                'no_warnings': True,
                'default_search': 'auto',
                'source_address': '0.0.0.0',
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.9',
                }
            }
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            video_file = FSInputFile("video.mp4")
            await message.answer_video(video_file, caption="Вот твое видео! Спасибо за подписку 👍")
            
            if os.path.exists("video.mp4"):
                os.remove("video.mp4")
        except Exception as e:
            await message.answer(f"❌ Произошла ошибка при скачивании: {e}")
    else:
        await message.answer("Пожалуйста, отправьте корректную ссылку на YouTube видео.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
