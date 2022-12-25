import json

from box import Box

with open('tgbot/locals/ru.json', encoding='utf-8') as file:
  stock = json.load(file)

data = Box(stock)

