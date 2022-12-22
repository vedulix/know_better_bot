from datetime import datetime
from telegraph import Telegraph
from tgbot.locals.load_json import data


def nice_date(dt):
  text = dt.strftime("%d ") + dt.strftime("%B")[:3]
  return text

def to_telegraph_link(page_name, html_content):
    html_content = html_content + data.html_end
    page_name = page_name + f" {str(datetime.now()).replace('.', '-')}"
    telegraph = Telegraph()
    telegraph.create_account(short_name=data.html_name)
    response = telegraph.create_page(page_name, html_content=html_content)

    return 'http://telegra.ph/{}'.format(response['path'])