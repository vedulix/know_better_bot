import random

from aiogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB
from tgbot.locals.load_json import data

#pear_keyboard = IKM(inline_keyboard=[[IKB(text="Посмотреть ответы", url="https:")]])
daily_ref_kb = IKM(inline_keyboard=[
  [
    IKB(text=data.jour.notif.change_time, callback_data="change_daily_ref_time"),
    #IKB(text=data.jour.notif.off, callback_data="off_notif"),
    IKB(text=data.jour.notif.see_all_ans, callback_data="see_all_ans"),
  ],
  [
    IKB(text=data.jour.notif.write, callback_data="write_daily_ref_ans"),
  ]
])

daily_ref_only_write_kb = IKM(inline_keyboard=[
  [
    IKB(text=data.jour.notif.write, callback_data="write_daily_ref_ans")
  ]
  ])



support_link_kb=IKM(inline_keyboard=[[IKB(text=data.support.inline_text, url=data.support.url)]])

need_help_link_kb=IKM(inline_keyboard=[[IKB(text=data.need_help.inline_text, url=data.need_help.url)]])



daily_back_kb = IKM(inline_keyboard=[
  [
    IKB(text=data.jour.notif.back, callback_data="back_daily_ref")
  ]])

timelist_kb = IKM(inline_keyboard=[
  [
    IKB(text="17:00", callback_data="time17"),
    IKB(text="18:00", callback_data="time18"),
    IKB(text="19:00", callback_data="time19"),
    IKB(text="20:00", callback_data="time20"),
    IKB(text="21:00", callback_data="time21"),
    IKB(text="22:00", callback_data="time22"),
  ],
   [
    IKB(text="23:00", callback_data="time23"),
    IKB(text="00:00", callback_data="time00"),
    IKB(text="01:00", callback_data="time01"),
    IKB(text="02:00", callback_data="time02"),
    IKB(text="03:00", callback_data="time03"),
    IKB(text="04:00", callback_data="time04"),
  ],
   [
    IKB(text="05:00", callback_data="time05"),
    IKB(text="06:00", callback_data="time06"),
    IKB(text="07:00", callback_data="time07"),
    IKB(text="08:00", callback_data="time08"),
    IKB(text="09:00", callback_data="time09"),
    IKB(text="10:00", callback_data="time10"),
  ],
   [
    IKB(text="11:00", callback_data="time11"),
    IKB(text="12:00", callback_data="time12"),
    IKB(text="13:00", callback_data="time13"),
    IKB(text="14:00", callback_data="time14"),
    IKB(text="15:00", callback_data="time15"),
    IKB(text="16:00", callback_data="time16"),
  ],
  [
    IKB(text=data.jour.notif.off, callback_data="off_notif")
  ]
])

