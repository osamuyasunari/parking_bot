from aiogram import types

def get_booking_keyboard(booking_data: dict[str, any]):
  available_places = []
  keyboard_markup = types.InlineKeyboardMarkup(row_width=3)
  for key, value in booking_data.items():
    if not value:
      available_places.append(key)

  place_btns = (types.InlineKeyboardButton(place, callback_data=place) for place in available_places)
  keyboard_markup.row(*place_btns)

  return keyboard_markup
