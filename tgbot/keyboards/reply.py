from aiogram.types import ReplyKeyboardMarkup as RKM, ReplyKeyboardRemove
from aiogram.types import KeyboardButton as kb


from tgbot.locals.load_json import data

def mkb(l):
  keyboard = RKM(keyboard=[[kb(row[i]) for i in range(len(row))] for row in l], resize_keyboard=True)
  return keyboard

#start keyboards


#whom = RKM(resize_keyboard=True).add(kb(data.know_better.whom.kb[0]), kb(data.know_better.whom.kb[1])).add(kb(data.know_better.whom.kb[2]), kb(data.know_better.whom.kb[3])).add(kb(data.know_better.whom.kb[4]))
