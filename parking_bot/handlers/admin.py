from aiogram import types, Dispatcher

from parking_bot.decorators import admin_only
from parking_bot.messages import messages
from parking_bot.models import Database

@admin_only
async def set_parking_places(message: types.Message, db: Database):
  parking_places = message.text.strip().lstrip("/set")
  if not len(parking_places):
    await message.reply(messages.INCORRECT_ARGUMENT)
  else:
    stripped = [place.strip() for place in parking_places.split(",")]
    db.parking_places = stripped
    await message.reply(messages.PLACES_SETTED)

def register_admin_handlers(dp: Dispatcher):
  dp.register_message_handler(set_parking_places, commands="set")