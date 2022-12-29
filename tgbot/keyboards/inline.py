from aiogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB
from tgbot.locals.load_json import data

#pear_keyboard = IKM(inline_keyboard=[[IKB(text="Посмотреть ответы", url="https://rozetka.com.ua/champion_a00225/p27223057")]])
daily_ref_kb = IKM(inline_keyboard=[
  [
    IKB(text=data.jour.notif.write, callback_data="write_daily_ref_ans"),
    IKB(text=data.jour.notif.change_time, callback_data="change_daily_ref_time")
  ],
  ])

daily_back_kb = IKM(inline_keyboard=[
  [
    IKB(text=data.jour.notif.back, callback_data="back_daily_ref")
  ]])

timelist_kb = IKM(inline_keyboard=[
  [
    IKB(text="17:00", callback_data="time"),
    IKB(text="18:00", callback_data="time"),
    IKB(text="19:00", callback_data="time"),
    IKB(text="20:00", callback_data="time"),
    IKB(text="21:00", callback_data="time"),
    IKB(text="22:00", callback_data="time"),
  ],
   [
    IKB(text="23:00", callback_data="time"),
    IKB(text="00:00", callback_data="time"),
    IKB(text="01:00", callback_data="time"),
    IKB(text="02:00", callback_data="time"),
    IKB(text="03:00", callback_data="time"),
    IKB(text="04:00", callback_data="time"),
  ],
   [
    IKB(text="05:00", callback_data="time"),
    IKB(text="06:00", callback_data="time"),
    IKB(text="07:00", callback_data="time"),
    IKB(text="08:00", callback_data="time"),
    IKB(text="09:00", callback_data="time"),
    IKB(text="10:00", callback_data="time"),
  ],
   [
    IKB(text="11:00", callback_data="time"),
    IKB(text="12:00", callback_data="time"),
    IKB(text="13:00", callback_data="time"),
    IKB(text="14:00", callback_data="time"),
    IKB(text="15:00", callback_data="time"),
    IKB(text="16:00", callback_data="time"),
  ],
  [
    IKB(text="Отключить напоминания ✖️", callback_data="off")
  ]
])

