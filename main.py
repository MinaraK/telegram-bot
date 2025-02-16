import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from datetime import datetime
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Создаем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_shift(date_str):
    try:
        base_date = datetime(2025, 2, 17)  # 17.02.2025 - вторая смена Минара
        input_date = datetime.strptime(date_str, "%d.%m.%Y")
        delta_days = (input_date - base_date).days
        shift_cycle = ["Вторая смена", "Выходной", "Первая смена"]
        shift = shift_cycle[delta_days % 3]
        weekdays = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        weekday = weekdays[input_date.weekday()]

        if shift == 'Первая смена':
            sabrin = 'Вторая смена'
            aylin = 'Выходной'
        elif shift == 'Вторая смена':
            sabrin = 'Выходной'
            aylin = 'Первая смена'
        elif shift == 'Выходной':
            sabrin = 'Первая смена'
            aylin = 'Вторая смена'

        return f"{date_str} - {weekday}.\nМинара - {shift}, Сабрин - {sabrin}, Айлин - {aylin}"
    except ValueError:
        return "Пожалуйста, введите дату в формате ДД.ММ.ГГГГ."

# Обработчик команд /start и /help
@dp.message(Command("start", "help"))
async def send_welcome(message: Message):
    await message.answer("Привет! Отправь мне дату в формате ДД.ММ.ГГГГ, и я скажу, какая у тебя смена.")

# Обработчик текстовых сообщений
@dp.message()
async def process_date(message: Message):
    response = get_shift(message.text)
    await message.answer(response)

# Функция запуска бота
async def main():
    await bot.delete_webhook(drop_pending_updates=True)  # Удаляем старые апдейты
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
