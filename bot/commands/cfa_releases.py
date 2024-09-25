from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram import Update
from telegram.ext import CallbackContext
import scraper_lib as scraper
import storage
import logging
import nlp

RIGHT_ARROW_SYMBOL = chr(8594) # →
LEFT_ARROW_SYMBOL = chr(8592) # ←
CFA_LAST_RELEASES_CALLBACK_ID = 'cfa_last_releases'

logger = logging.getLogger(__name__)

import datetime
from uuid import uuid4

class Post:
  def __init__(self, post_items, post_id=None, creation_time=None, page_items_cnt=4):
    self._items_count_on_page = page_items_cnt
    self._current_page = 0
    self.post_id = post_id or str(uuid4())
    self.post_items = post_items
    self.pages = [
      self.post_items[i:i+self._items_count_on_page]
      for i in range(0, len(self.post_items), self._items_count_on_page)
    ]
    self._pages_cnt = len(self.pages) - 1
    self.creation_time = creation_time or datetime.datetime.now()

  def current_page(self):
    return self.pages[self._current_page]

  def next_page(self):
    if self._current_page == self._pages_cnt:
      self._current_page = 0
    else:
      self._current_page += 1
    return self.pages[self._current_page]

  def previous_page(self):
    if self._current_page == 0:
      self._current_page = self._pages_cnt
    else:
      self._current_page -= 1
    return self.pages[self._current_page]

  @property
  def current_stage_text(self):
    return f'{self.current_page_number}/{self.pages_count}'
  
  @property
  def pages_count(self):
    return self._pages_cnt + 1

  @property
  def current_page_number(self):
    return self._current_page + 1

  @property
  def items_count_on_page(self):
    return self._items_count_on_page

def get_releases_post_markup(post):
  def release_ner_markup(d):
    d = d.to_dict()
    if d['date_time_placement_start'] is None:
      return 'Описание не найдено.'
    start = d.get("date_time_placement_start").replace('МСК','')
    end = d.get("date_time_placement_end").replace('МСК','')
    bod = d.get("cfa_repayment_date_time").replace('МСК','')
    r = (f'<b>Кол-во:</b> {int(d.get("cfa_count")):_} шт.\n'
        f'<b>Цена:</b> {d.get("cfa_price")}\n'
        f'<b>Начало размещения:</b> {start}\n'
        f'<b>Окончаниe размещения:</b> {end}\n'
        f'<b>Погашение тела:</b> {bod}\n'
        f'<b>Период выплаты купонов:</b> {d.get("coupon_period")}\n'
        f'<b>Способ погашения:</b> {d.get("cfa_repayment_method")}')
    return r
  msg_text = '\n\n'.join(
    f'{n}. <a href="{release.url}"> {release.title} </a>\n'
    f'<b>Платформа:</b> {release.platform_name}.\n'
    f'<b>Опубликовано:</b> {release.release_time.strftime("%Y-%m-%d")}.\n'
    f'{release_ner_markup(release)}'
    for n, release in enumerate(
      post.current_page(),
      start=(post.current_page_number - 1) * post.items_count_on_page + 1
    )
  )
  callback_id = CFA_LAST_RELEASES_CALLBACK_ID
  internal_post_id = post.post_id
  keyboard = [
    [
      InlineKeyboardButton(LEFT_ARROW_SYMBOL, callback_data=f'{callback_id}_backward_{internal_post_id}'),
      InlineKeyboardButton(post.current_stage_text, callback_data=f'{callback_id}_counter_{internal_post_id}'),
      InlineKeyboardButton(RIGHT_ARROW_SYMBOL, callback_data=f'{callback_id}_forward_{internal_post_id}'),
    ],
  ]
  keyboard_markup = InlineKeyboardMarkup(keyboard)
  return msg_text, keyboard_markup

def cfa_command_dispetcher(func):
  async def wrapper(update, context_or_target_chat_id=None):
    if isinstance(update, Update) and isinstance(context_or_target_chat_id, CallbackContext):
      target_chat_id = update.effective_chat.id 
      context = context_or_target_chat_id
    else:
      target_chat_id = context_or_target_chat_id 
      context = update
    await func(context, target_chat_id)
  return wrapper

@cfa_command_dispetcher
async def cfa_releases(context, target_chat_id):
  effective_chat_id = target_chat_id
  releases = storage.get_last_24h_releases()
  logger.info(f'releases cnt in cmd {len(releases)}')
  #releases = storage.get_n_releases()
  releases = sorted(releases, key=lambda a: a.release_time, reverse=True)
  if len(releases) == 0:
    await context.bot.send_message(
      chat_id=effective_chat_id,
      text='Выпуски ЦФА за сутки не найдены.',
    )
    return
  post = Post(
    post_items=sorted(releases, key=lambda x: x.platform_name),
    page_items_cnt=2,
  )
  # Save post to cache
  #context.bot_data['post_cache'][post.post_id] = post # bot cache
  storage.redis_client.set_complex_obj(post.post_id, post) # redis cache
  # Save post to db
  storage.add_releases_posts([{'bot_post_id': post.post_id, 'release_id': rel.db_id} for rel in releases])
  msg_text, keyboard = get_releases_post_markup(post)
  await context.bot.send_message(
    chat_id=effective_chat_id,
    text=msg_text,
    reply_markup=keyboard,
    parse_mode=ParseMode.HTML,
    disable_web_page_preview=True,
  )

async def cfa_last_releases_button_callback(update, context):
  query = update.callback_query
  btn_name = query.data
  keyboard_action, post_id = btn_name.replace(CFA_LAST_RELEASES_CALLBACK_ID + '_', '').split('_')
  # Get post from cache
  #post = context.bot_data['post_cache'].get(post_id) # bot cache
  post = storage.redis_client.get_complex_obj(post_id) # redis cache
  if post is None:
    post_releases = storage.get_releases_by_release_post(post_id)
    #post_releases = []
    if len(post_releases) == 0:
      await context.bot.send_message(
        chat_id=query.message.chat.id,
        reply_to_message_id=query.message.message_id,
        text='По некоторым причинам кеш этого поста не найден, поэтому действие недоступно.'
      )
      return
    post = Post(post_items=post_releases, post_id=post_id, page_items_cnt=2)
  if post.pages_count == 1:
    return
  match keyboard_action:
    case 'counter':
      return
    case 'forward':
      post.next_page()
    case 'backward':
      post.previous_page()
  storage.redis_client.set_complex_obj(post_id, post)
  msg_text, keyboard = get_releases_post_markup(post)
  await query.edit_message_text(
    text=msg_text,
    reply_markup=keyboard,
    parse_mode=ParseMode.HTML,
    disable_web_page_preview=True,
  )

