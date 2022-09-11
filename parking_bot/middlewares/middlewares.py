from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram import Bot

from parking_bot.models.database import Database
from parking_bot.utils import Notifier

class SharedDataMiddleware(LifetimeControllerMiddleware):
  skip_patterns = ["error", "update"]

  def __init__(self, bot: Bot, db: Database, notifier: Notifier):
      super().__init__()
      self.bot = bot
      self.db = db
      self.notifier = notifier

  async def pre_process(self, obj, data, *args):
      data["db"] = self.db
      data["bot"] = self.bot
      data["notifier"] = self.notifier