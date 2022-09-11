def getStartMessage(full_name: str, isAdmin: bool) -> str:
  start_message = f"""
Привет {full_name}!
Это бот бронирования мест на парковке Кроноса.
Доступные команды:
/info - забронированые места
/book - забронировать место
/unbook - снять бронь
/subscribe - подписаться на оповещения
/unsubscribe - отписаться от оповещений
"""
  if isAdmin:
    start_message += """
Команды админа:
/set - задать парковочные места    
"""

  return start_message

ADMIN_NOT_SET_PLACES = "Места пока что не заполнены администратором!"
PLACES_SETTED = "Места заданы"
UNAUTHORIZED = "У вас нет подходящих прав"
CHOOSE_PLACE = "Выберите свободное место"
NONEXISTING_PLACE = "Некорректное место"
ALL_PLACES_BOOKED = "Свободные места закончились 😔"
PLACE_BOOKED = lambda place: f"Место {place} забронировано!"
PLACE_UNBOOKED = lambda place: f"Место {place} снова доступно для бронирования"
PLACE_ALREADY_BOOKED = lambda place: f"Место {place} уже занято, выберите другое!"
USER_ALREADY_BOOKED = lambda place: f"Нельзя бронировать больше одного места. Вы уже заняли место {place}."
USER_NOT_BOOKED = "У вас нет забронированных мест"
SUBSCRIBE_SUCCESS = "Вы подписаны на рассылку"
ALREADY_SUBSCRIBED = "Вы уже подписаны на рассылку"
UNSUBSCRIBE_SUCCESS = "Вы отписаны от рассылки"
ALREADY_UNSUBSCRIBED = "Вы не подписаны на рассылку"

UNBOOK_ALERT = lambda place: f"Место {place} снова доступно для бронирования!"
BOOK_ALERT = lambda place, full_name: f"Место {place} забронировано пользователем {full_name}"
RESET_ALERT = lambda places: f"""
Сброс брони!
Места {places} снова доступны для бронирования.
"""
INCORRECT_ARGUMENT = "Некорректный аргумент"