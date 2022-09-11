import asyncio
from typing import Optional
from aiogram.bot import Bot

from parking_bot.models import Database

TIMEOUT = .05

class Notifier:
  def __init__(self, db: Database, bot: Bot):
    self.db = db
    self.bot = bot

  async def notify(self, message: str, current_user: Optional[int] = None):
    alert_list = self.db.alert_list

    for user_id in alert_list:
      if current_user and user_id == current_user:
        pass
      else:
        await self.bot.send_message(user_id, message)
        await asyncio.sleep(TIMEOUT) # 20 messages per second (Limit: 30 messages per second)
