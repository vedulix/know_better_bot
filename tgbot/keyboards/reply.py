from aiogram.types import ReplyKeyboardMarkup as RKM, ReplyKeyboardRemove
from aiogram.types import KeyboardButton as kb


from tgbot.locals.load_json import data

def mkb(l):
  keyboard = RKM(keyboard=[[kb(row[i]) for i in range(len(row))] for row in l], resize_keyboard=True)
  return keyboard

#start keyboards
s1 = RKM(resize_keyboard=True).add(kb(data.start.hi.kb))
s2 = RKM(resize_keyboard=True).add(kb(data.start.ask_question_how.kb))
s3 = RKM(resize_keyboard=True).add(kb(data.start.ask_question_for_whom.kb))
s4 = RKM(resize_keyboard=True).add(kb(data.start.to_main_menu.kb[0])).add(kb(data.start.to_main_menu.kb[1]), kb(data.start.to_main_menu.kb[2]))


#know_better keyboards
whom = RKM(resize_keyboard=True).add(kb(data.know_better.whom.kb[0]), kb(data.know_better.whom.kb[1])).add(kb(data.know_better.whom.kb[2]), kb(data.know_better.whom.kb[3])).add(kb(data.know_better.whom.kb[4]))
next_question=RKM(resize_keyboard=True).add(kb(data.know_better.questions.kb[0])).add(kb(data.know_better.questions.kb[1]), kb(data.know_better.questions.kb[2]))
#next_sub_question=RKM(resize_keyboard=True).add(kb(data.know_better.sub_questions.kb[0])).add(kb(data.know_better.sub_questions.kb[1]), kb(data.know_better.sub_questions.kb[2]))
partner_choose_kb= RKM(resize_keyboard=True).add(kb(data.know_better.partner.choose.kb[0]), kb(data.know_better.partner.choose.kb[1]), kb(data.know_better.partner.choose.kb[2])).add(kb(data.know_better.partner.choose.kb[3]))
friend_choose_kb = RKM(resize_keyboard=True).add(kb(data.know_better.friend.choose.kb[0]),kb(data.know_better.friend.choose.kb[1])).add(kb(data.know_better.friend.choose.kb[2]))


work_hi_kb = RKM(resize_keyboard=True).add(kb(data.know_better.sub_questions.hi.kb[0])).add(kb(data.know_better.sub_questions.hi.kb[1]))
work_kb = RKM(resize_keyboard=True).add(kb(data.know_better.sub_questions.work.kb[0]), kb(data.know_better.sub_questions.work.kb[1])).add(kb(data.know_better.sub_questions.work.kb[2]))

#journaling keyboards
choose_jour = RKM(resize_keyboard=True).add(kb(data.jour.choose.kb[0]), kb(data.jour.choose.kb[1])).add(kb(data.main_menu.text_to))
self_hi = RKM(resize_keyboard=True).add(kb(data.jour.myself.hi.kb[0]), kb(data.jour.myself.hi.kb[1])).add(kb(data.jour.myself.hi.kb[2]))
sub_hi = RKM(resize_keyboard=True).add(kb(data.jour.sub.hi.kb[0]), kb(data.jour.sub.hi.kb[1])).add(kb(data.jour.sub.hi.kb[2]))
year_hi_kb=mkb(data.jour.year.hi.kb)

work_ans_kb = RKM(resize_keyboard=True, input_field_placeholder=data.jour.sub.work_ans.placeholder).add(kb(data.jour.sub.work_ans.kb[0]), kb(data.jour.sub.work_ans.kb[1]))
#work_ans_kb = ReplyKeyboardRemove().add(kb(data.know_better.sub_questions.work_ans.kb[0]), kb(data.know_better.sub_questions.work_ans.kb[1])).add(kb(data.know_better.sub_questions.work_ans.kb[2]))

#main_menu
rec_choose = RKM(resize_keyboard=True).add(kb(data.rec.choose.kb[0]), kb(data.rec.choose.kb[1])).add(kb(data.rec.choose.kb[2]))
about_bot_kb = RKM(resize_keyboard=True).add(kb(data.about_bot.kb[0]))
main_menu_buttons = RKM(resize_keyboard=True).add(kb(data.main_menu.kb[0]), kb(data.main_menu.kb[1])).add(kb(data.main_menu.kb[2]), kb(data.main_menu.kb[3]))


#active listening
al_kb_1 = RKM(resize_keyboard=True).add(kb(data.rec.actlis.pre_define.kb[0])).add(kb(data.rec.actlis.pre_define.kb[1]))
al_kb_2 = RKM(resize_keyboard=True).add(kb(data.rec.actlis.define.kb[0]))
al_kb_3 = RKM(resize_keyboard=True).add(kb(data.rec.actlis.factors.kb[0]))
al_kb_4 = RKM(resize_keyboard=True).add(kb(data.rec.actlis.method_1.kb[0]))
al_kb_5 = RKM(resize_keyboard=True).add(kb(data.rec.actlis.method_2.kb[0]))
al_kb_6 = RKM(resize_keyboard=True).add(kb(data.rec.actlis.method_3.kb[0]))
al_kb_7 = RKM(resize_keyboard=True).add(kb(data.rec.actlis.advice.kb[0]))


#nonviolent communication
nvc_kb_1 = RKM(resize_keyboard=True).add(kb(data.rec.nvc.define.kb[0])).add(kb(data.rec.nvc.define.kb[1]))
nvc_kb_2 = RKM(resize_keyboard=True).add(kb(data.rec.nvc.n1.kb[0]))
nvc_kb_3 = RKM(resize_keyboard=True).add(kb(data.rec.nvc.n2.kb[0]))
nvc_kb_4 = RKM(resize_keyboard=True).add(kb(data.rec.nvc.n3.kb[0]))
nvc_kb_5 = RKM(resize_keyboard=True).add(kb(data.rec.nvc.n4.kb[0])).add(kb(data.rec.nvc.n4.kb[1]))
nvc_kb_6 = RKM(resize_keyboard=True).add(kb(data.rec.nvc.example.kb[0]))
