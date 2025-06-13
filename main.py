import asyncio
from aiogram import Bot, Dispatcher
from handlers import main_menu, other, begin
import push
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import time
import os
# Объект бота

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
NOTIFICATION_TIME = time(hour=9, minute=0)  # Время уведомлений (09:30)
scheduler = AsyncIOScheduler()
# Диспетчер
dp = Dispatcher()

dp.include_routers(begin.router, main_menu.router, other.router)

async def send_push():
    await push.mainPush(bot)

# Запуск планировщика
def start_scheduler():
    scheduler.add_job(
        send_push,
        'cron',
        hour=NOTIFICATION_TIME.hour,
        minute=NOTIFICATION_TIME.minute
    )
    scheduler.start()

# Запуск процесса поллинга новых апдейтов
async def main():
    # await push.mainPush(bot)
    start_scheduler()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())