from aiogram import types

from parking_bot.utils import admin_check
from parking_bot.messages import messages
from parking_bot.models import Database

def admin_only(func):
  async def inner(message: types.Message, db: Database):
    if (admin_check(message.from_user.username, db.admins)):
      return await func(message, db)
    else:
      await message.reply(messages.UNAUTHORIZED)
  return inner