from typing import Optional
from .user import User

class Database:
  __parking_places: list[str]
  booking_data: dict[str, Optional[User]]
  alert_list: list[int]
  admins: list[str]

  def __init__(self):
    self.__parking_places = []
    self.booking_data = {}
    self.alert_list = []
    self.admins = []
    self.reset()

  @property
  def parking_places(self):
    return self.__parking_places

  @parking_places.setter
  def parking_places(self, value: list[str]):
    self.__parking_places = list(set(value))
    if len(value):
      self.reset()
    else:
      self.booking_data = {}

  @parking_places.deleter
  def parking_places(self):
    self.__parking_places = []

  def reset(self):
    self.booking_data = {}
    for place in self.__parking_places:
      self.booking_data[place] = None
