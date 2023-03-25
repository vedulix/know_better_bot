from aiogram.dispatcher.filters.state import StatesGroup, State

#start states
class Start(StatesGroup):
  s1=State()
  s2=State()




class Mail(StatesGroup):
  wait = State()

