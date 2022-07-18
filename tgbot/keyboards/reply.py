from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tgbot.locals.load_json import data


#start keyboards
s1 = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(data.start.hi.kb))
s2 = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(data.start.ask_question_how.kb))
s3 = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(data.start.ask_question_for_whom.kb))
s4 = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(data.start.to_main_menu.kb[0])).add(KeyboardButton(data.start.to_main_menu.kb[1]), KeyboardButton(data.start.to_main_menu.kb[2]))


#know_better keyboards
whom = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(data.know_better.whom.kb[0]), KeyboardButton(data.know_better.whom.kb[1])).add(KeyboardButton(data.know_better.whom.kb[2]), KeyboardButton(data.know_better.whom.kb[3])).add(KeyboardButton(data.know_better.whom.kb[4]))
next_question=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(data.know_better.questions.kb[0])).add(KeyboardButton(data.know_better.questions.kb[1]), KeyboardButton(data.know_better.questions.kb[2]))


#main_menu
rec_choose = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(data.rec.choose.kb[0]), KeyboardButton(data.rec.choose.kb[1])).add(KeyboardButton(data.rec.choose.kb[2]))
about_bot_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(data.about_bot.kb[0]))
main_menu_buttons = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(data.main_menu.kb[0])).add(KeyboardButton(data.main_menu.kb[1]), KeyboardButton(data.main_menu.kb[2]))


#active listening
al_kb_1 = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(data.rec.actlis.pre_define.kb[0])).add(KeyboardButton(data.rec.actlis.pre_define.kb[1]))
al_kb_2 = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(data.rec.actlis.define.kb[0]))
al_kb_3 = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(data.rec.actlis.factors.kb[0]))
al_kb_4 = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(data.rec.actlis.method_1.kb[0]))
al_kb_5 = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(data.rec.actlis.method_2.kb[0]))
al_kb_6 = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(data.rec.actlis.method_3.kb[0]))
al_kb_7 = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(data.rec.actlis.advice.kb[0]))


#nonviolent communication
nvc_kb_1 = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(data.rec.nvc.define.kb[0])).add(KeyboardButton(data.rec.nvc.define.kb[1]))
nvc_kb_2 = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(data.rec.nvc.n1.kb[0]))
nvc_kb_3 = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(data.rec.nvc.n2.kb[0]))
nvc_kb_4 = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(data.rec.nvc.n3.kb[0]))
nvc_kb_5 = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(data.rec.nvc.n4.kb[0])).add(KeyboardButton(data.rec.nvc.n4.kb[1]))
nvc_kb_6 = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(data.rec.nvc.example.kb[0]))
