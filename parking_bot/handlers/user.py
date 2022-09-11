from aiogram import types, Bot, Dispatcher, filters

from parking_bot.utils import get_booking_keyboard, admin_check
from parking_bot.messages import messages
from parking_bot.models import Database, User
from parking_bot.utils import Notifier

async def start(message: types.Message, db: Database):
  isAdmin = admin_check(message.from_user.username, db.admins)
  await message.reply(messages.getStartMessage(message.from_user.full_name, isAdmin))

async def info(message: types.Message, db: Database):
  answer = ""
  for place, user in db.booking_data.items():
    state = user.full_name if user else "Свободно"
    answer += f"{place}: {state}\n"

  if (len(answer) == 0):
    answer = messages.ADMIN_NOT_SET_PLACES

  await message.reply(answer)

async def book(message: types.Message, db: Database):
  available_places = []
  for place, value in db.booking_data.items():
    if not value:
      available_places.append(place)
    else:
      if value.username == message.from_user.username:
        await message.reply(messages.USER_ALREADY_BOOKED(place))
        return

  if len(available_places):
    await message.reply(messages.CHOOSE_PLACE, reply_markup=get_booking_keyboard(db.booking_data))
  else:
    await message.reply(messages.ALL_PLACES_BOOKED)

async def unbook(message: types.Message, db: Database, notifier: Notifier):
  username = message.from_user.username

  for place, user in db.booking_data.items():
    if user and user.username == username:
      db.booking_data[place] = None
      await message.reply(messages.PLACE_UNBOOKED(place))
      await notifier.notify(messages.UNBOOK_ALERT(place), message.from_id)
      return
  
  await message.reply(messages.USER_NOT_BOOKED)

async def subscribe(message: types.Message, db: Database):
  user_id = message.from_id

  if user_id in db.alert_list:
    await message.reply(messages.ALREADY_SUBSCRIBED)
  else:
    db.alert_list.append(user_id)
    await message.reply(messages.SUBSCRIBE_SUCCESS)
    
async def unsubscribe(message: types.Message, db: Database):
  user_id = message.from_id
  
  if user_id in db.alert_list:
    db.alert_list.remove(user_id)
    await message.reply(messages.UNSUBSCRIBE_SUCCESS)
  else:
    await message.reply(messages.ALREADY_UNSUBSCRIBED)

async def callback_vote_action(query: types.CallbackQuery, db: Database, bot: Bot, notifier: Notifier):
  picked_place = query.data
  await query.answer()
  available_places = []

  for place, value in db.booking_data.items():
    if not value:
      available_places.append(place)

  if picked_place in db.booking_data.keys():

    if picked_place in available_places:
      user = query.from_user
      db.booking_data[picked_place] = User(
        username=user.username,
        full_name=user.full_name
      )
      await bot.edit_message_text(
        messages.PLACE_BOOKED(picked_place),
        query.from_user.id,
        query.message.message_id,
      )
      await notifier.notify(messages.BOOK_ALERT(picked_place, user.full_name), user.id)
    else:
      await bot.edit_message_text(
        messages.PLACE_ALREADY_BOOKED(picked_place),
        query.from_user.id,
        query.message.message_id,
        reply_markup=get_booking_keyboard(db.booking_data)
      )

  else:
    await bot.edit_message_text(
      messages.NONEXISTING_PLACE,
      query.from_user.id,
      query.message.message_id,
    )

def register_user_handlers(dp: Dispatcher):
  dp.register_message_handler(start, commands=["start", "help"])
  dp.register_message_handler(info, commands="info")
  dp.register_message_handler(book, commands="book")
  dp.register_message_handler(unbook, commands="unbook")
  dp.register_message_handler(subscribe, commands="subscribe")
  dp.register_message_handler(unsubscribe, commands="unsubscribe")
  dp.register_callback_query_handler(callback_vote_action, filters.Regexp(r"\d*"))