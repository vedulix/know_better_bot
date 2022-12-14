from aiogram.dispatcher.filters.state import StatesGroup, State

#start states
class Start(StatesGroup):
  s1=State()
  s2=State()
  s3=State()

class main_menu_states(StatesGroup):
  rec = State()
  about = State()

class Know(StatesGroup):
  whom = State()
  myself = State()
  partner = State()
  partner_test = State()
  partner_choose = State()
  friend_choose = State()
  work = State()
  work_ans = State()
  family = State()
  friend = State()

class actlis_states(StatesGroup):
  al1 = State()
  al2 = State()
  al3 = State()
  al4 = State()
  al5 = State()
  al6 = State()
  al7 = State()

class nvc_states(StatesGroup):
  n1 = State()
  n2 = State()
  n3 = State()
  n4 = State()
  n5 = State()
  n6 = State()
