with open("tgbot/locals/ru_myself.txt", encoding='utf-8') as file:
  questions_myself = [row.strip() for row in file]


with open("tgbot/locals/ru_partner.txt", encoding='utf-8') as file:
  questions_partner = [row.strip() for row in file]

with open("tgbot/locals/ru_partner_test.txt", encoding='utf-8') as file:
  questions_partner_test = [row.strip() for row in file]


with open("tgbot/locals/ru_family.txt", encoding='utf-8') as file:
  questions_family = [row.strip() for row in file]


with open("tgbot/locals/ru_friend.txt", encoding='utf-8') as file:
  questions_friend = [row.strip() for row in file]
