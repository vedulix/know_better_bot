from datetime import datetime
from telegraph import Telegraph
from tgbot.locals.load_json import data


def nice_date(dt):
  text = dt.strftime("%d ") + dt.strftime("%B")[:3]
  return text

def delete_commands(s):
    if (x in s for x in ['feelings', 'states', 'needs']):
        s = s.replace('Нажми /feelings, чтобы посмотреть список основных чувств', '')
        s = s.replace('Нажми /needs, чтобы посмотреть список основных потребностей', '')
        s = s.replace('Нажми /states, чтобы посмотреть список основных состояний', '')
    return s

def to_telegraph_link(page_name, html_content):
    html_content = html_content + data.html_end
    page_name = page_name + f" {str(datetime.now()).replace('.', '-')}"
    telegraph = Telegraph()
    telegraph.create_account(short_name=data.html_name)
    response = telegraph.create_page(page_name, html_content=html_content)

    return 'http://telegra.ph/{}'.format(response['path'])