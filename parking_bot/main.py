import asyncio
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import logging
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from parking_bot.handlers import user, admin
from parking_bot.middlewares import SharedDataMiddleware
from parking_bot.models import Database
from parking_bot.utils import Notifier
from parking_bot.messages import messages

token = os.getenv("PARKING_BOT_API_TOKEN")
logger = logging.getLogger(__name__)

if not token:
  logger.error("API token not provided. Set it by env PARKING_BOT_API_TOKEN.")
  sys.exit()

async def reset(notifier: Notifier, db: Database):
  db.reset()
  await notifier.notify(messages.RESET_ALERT(", ".join(db.parking_places)))

async def main():
  logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
  )
  logger.info("Starting bot")

  bot = Bot(token=token)
  scheduler = AsyncIOScheduler()
  dp = Dispatcher(bot)
  db = Database()
  notifier = Notifier(db, bot)

  shared_data_middleware = SharedDataMiddleware(bot, db, notifier)
  dp.middleware.setup(shared_data_middleware)

  user.register_user_handlers(dp)
  admin.register_admin_handlers(dp)

  scheduler.add_job(reset, CronTrigger.from_crontab("0 8 * * 1-6", timezone="Asia/Novosibirsk"), args=(notifier, db))
  scheduler.start()

  try:
    await dp.start_polling()
  finally:
    await bot.get_session().close()

def main_wrapper():
  try:
    asyncio.run(main())
  except (KeyboardInterrupt, SystemExit):
    logger.error("Bot stopped!")

if __name__ == "__main__":
  main_wrapper()