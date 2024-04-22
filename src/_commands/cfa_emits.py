from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging
import datetime
import time
import requests
from bs4 import BeautifulSoup, SoupStrainer
from collections import defaultdict
import re
import urllib

logger = logging.getLogger(__name__)

_platform_mapping = {
  'На платформе А-Токен': ('А-Токен', 'atoken'),
  'На платформе Атомайз': ('Атомайз', 'atomayz'),
  'На платформе Еврофинанс Моснарбанк': ('Еврофинанс Моснарбанк', 'evrofinance'),
  'На платформе Лайтхаус': ('Лайтхаус', 'litehouse'),
  'На платформе Мастерчейн': ('Мастерчейн', 'masterchain'),
  'На платформе Мосбиржа/НРД': ('Мосбиржа/НРД', 'mosbirja'),
  'На платформе СПБ Биржа': ('СПБ Биржа', 'spbbirja'),
  'На платформе Сбер': ('Сбер', 'sber'),
  'На платформе Токеон': ('Токеон', 'tokeon'),
  'Платформа ЦФА ХАБ': ('ЦФА ХАБ', 'cfahub')
}
_btnid_x_emitn_mapping = {
  'atoken': 'На платформе А-Токен',
  'atomayz': 'На платформе Атомайз',
  'cfahub': 'Платформа ЦФА ХАБ',
  'evrofinance': 'На платформе Еврофинанс Моснарбанк',
  'litehouse': 'На платформе Лайтхаус',
  'masterchain': 'На платформе Мастерчейн',
  'mosbirja': 'На платформе Мосбиржа/НРД',
  'sber': 'На платформе Сбер',
  'spbbirja': 'На платформе СПБ Биржа',
  'tokeon': 'На платформе Токеон'
}

def fetch_emits():
  def fetch_cfa_ru_html():
    url = 'https://цфа.рф/cfa-vypusk.html'
    res = requests.get(url)
    res.encoding = 'utf-8'
    html = res.text
    logger.info(f'Fetch emits {res.url}')
    logger.info(f'Fetch emits with status {res.status_code}')
    logger.info(f'Fetch emits in {res.elapsed.total_seconds()} seconds')
    return html

  def parse_emits_page(html):
    only_tags_with_id_imcontent = SoupStrainer('main', {'id': 'imContent'})
    soup = BeautifulSoup(
      markup=html,
      features='lxml',
      parse_only=only_tags_with_id_imcontent,
    )
    platform_headings = soup.find_all('h3', {'class': 'imHeading3'})
    emits_by_platform = { heading.get_text(): heading.parent for heading in platform_headings }

    def parse_platform(platform_div):
      site_url = 'https://цфа.рф/'
      date_pattern = re.compile(r'^(3[01]|[12][0-9]|0[1-9]).(1[0-2]|0[1-9]).[0-9]{4}$')
      last_date = None
      last_span_header = None
      date_emits = defaultdict(lambda: defaultdict(set))
      for nxt in platform_div.find_all(['span', 'li']):
        span_text = nxt.get_text()
        span_text = span_text.strip()
        if span_text == '':
          continue
        is_date = date_pattern.match(span_text)
        if is_date:
          last_date = span_text
          last_span_header = None
        else:
          is_span_header = not any(parent.name == 'li' for n, parent in zip(range(3), nxt.parents))
          if is_span_header and nxt.name =='span':
            last_span_header = span_text
          else:
            tag_a = nxt.find('a')
            if tag_a is None:
              continue
            emit_name = tag_a.get_text()
            emit_href = tag_a.get('href')
            emit_href = urllib.parse.urljoin(site_url, emit_href)
            if last_span_header:
              date_emits[last_date][(last_span_header, emit_name)].add(emit_href)
            else:
              date_emits[last_date][emit_name].add(emit_href)
      return date_emits
    result_emits_by_platform = dict()
    for platform_name, platform_emits_div in emits_by_platform.items():
      platform_emits = parse_platform(platform_emits_div)         
      result_emits_by_platform[platform_name] = platform_emits
    return result_emits_by_platform
  html = fetch_cfa_ru_html()
  emits = parse_emits_page(html)
  return emits

def get_emit(context, by='today'):
  emits = fetch_emits()
  context.bot_data['emits_cache'] = emits 
  plt_name = _btnid_x_emitn_mapping.get(by)
  msg = ''
  for platform_name, emits in emits.items():
    if platform_name != plt_name:
      continue 
    msg += f'{platform_name}\n'
    for emit_date, date_emits in emits.items():
      msg += f'\t{emit_date}\n' 
      for emit_name, emit_href in date_emits.items():
        if isinstance(emit_name, tuple):
          emit_name = ', '.join(emit_name)
        emit_href = list(emit_href)[0]
        msg += f'\t\t{emit_name} - {emit_href}\n' 
  return msg

def get_keyboard(unix_ts=None):
  unix_ts = unix_ts or int(time.mktime(datetime.datetime.now().timetuple()))
  pagination_keyboard = [
    *[
      [InlineKeyboardButton(platform_name, callback_data=f'emits_{unix_ts}_{eid}') for (platform_name, eid) in list(_platform_mapping.values())[i:i+3]]
      for i in range(0, len(_platform_mapping), 3)
    ]
  ]
  keyboard_markup = InlineKeyboardMarkup(pagination_keyboard)
  return keyboard_markup

def get_text(platform_name, context):
  logger.info(f'Get text {platform_name}')
  emit = get_emit(context=context, by=platform_name)
  if len(emit) > 4096:
    emit = emit[:4000]
    emit += '\n**Указаны не все новости из-за размера. Будет исправлено позже**'
  return emit

async def cfa_emits_button_callback(update, context, query, btn_data):
  logger.info(f'emits btn {btn_data!r} clicked')
  btn_cls, ts, val = btn_data.split('_')
  ts = int(ts)
  if (datetime.datetime.now() - datetime.datetime.fromtimestamp(ts)).seconds // 60 > 60:
    await context.bot.send_message(
      chat_id=query.message.chat.id,
      reply_to_message_id=query.message.message_id,
      text='По некоторым причинам кеш этого поста не найден, поэтому действие недоступно.'
    )
    return
  keyboard_markup = get_keyboard(ts)
  post_markup = get_text(platform_name=val, context=context)
  await query.edit_message_text(
    text=post_markup,
    disable_web_page_preview=True,
    reply_markup=keyboard_markup,
  )

async def cfa_emits(update, context):
  txt = get_text(platform_name='sber', context=context)
  keyboard_markup = get_keyboard()
  await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text=txt,
    reply_markup=keyboard_markup,
  )
  