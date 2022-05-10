import logging
import requests
from bs4 import BeautifulSoup
import datetime
from aiogram import Bot, Dispatcher, executor, types

from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()
API_TOKEN = '5068486190:AAFQ6MCmqnimn-A8WMhlvhDK9sSEqnq5nSo'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)



logging.basicConfig(level=logging.INFO)


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    global admin_id
    admin_id = message.chat.id
    scheduler.add_job(send_message_to_admin, "cron", hour='05', minute='00', args=(bot,))
    scheduler.start()
    await message.reply("Бот запущен!", chat_id="")




async def send_message_to_admin(bot: Bot):
    response = requests.get("https://www.akchabar.kg/ru/exchange-rates/dollar/")
    soup = BeautifulSoup(response.text, 'lxml')
    body = soup.find_all("tr")
    f = ''

    for i in body:

        if " ".join(item.strip() for item in i.find_all(text=True)) in f:
            print()
            break
        else:
            pass
        f += " ".join(item.strip() for item in i.find_all(text=True))
        f += "\n\n"

    await bot.send_message(text=f, chat_id=admin_id)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)