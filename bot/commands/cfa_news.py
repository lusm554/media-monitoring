from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
import scraper_lib as scraper
from storage import postgres_client
import logging

RIGHT_ARROW_SYMBOL = chr(8594) # →
LEFT_ARROW_SYMBOL = chr(8592) # ←
CFA_LAST_NEWS_CALLBACK_ID = 'cfa_last_news'

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

def get_cfa_last_news_post_markup(post):
  msg = '\n\n'.join(
    f'{n}. <a href="{article.url}"> {article.title} </a>\n'
    f'<b>Источник:</b> {article.publisher_name}.\n'
    f'<b>Опубликовано:</b> {article.publish_time}.\n'
    f'<b>Взято из:</b> {article.scraper}.'
    for n, article in enumerate(
      post.current_page(),
      start=(post.current_page_number - 1) * post.items_count_on_page + 1
    )
  )
  internal_post_id = post.post_id
  callback_id = CFA_LAST_NEWS_CALLBACK_ID
  pagination_keyboard = [
    [
      InlineKeyboardButton(LEFT_ARROW_SYMBOL, callback_data=f'{callback_id}_backward_{internal_post_id}'),
      InlineKeyboardButton(post.current_stage_text, callback_data=f'{callback_id}_counter_{internal_post_id}'),
      InlineKeyboardButton(RIGHT_ARROW_SYMBOL, callback_data=f'{callback_id}_forward_{internal_post_id}')
    ],
  ]
  keyboard_markup = InlineKeyboardMarkup(pagination_keyboard)
  return msg, keyboard_markup

def cfa_command_dispetcher(func):
  from telegram import Update
  from telegram.ext import CallbackContext
  async def wrapper(update, context_or_target_chat_id=None):
    print()
    print(update, context_or_target_chat_id)
    print()
    if isinstance(update, Update) and isinstance(context_or_target_chat_id, CallbackContext):
      print(1)
      target_chat_id = update.effective_chat.id 
      context = context_or_target_chat_id
    else:
      print(2)
      target_chat_id = context_or_target_chat_id 
      context = update
    print()
    print(type(update), type(context_or_target_chat_id))
    print(update, context_or_target_chat_id)
    print()
    await func(context, target_chat_id)
  return wrapper


# <class 'telegram._update.Update'> <class 'telegram.ext._callbackcontext.CallbackContext'>
# <class 'telegram.ext._callbackcontext.CallbackContext'> <class 'NoneType'>

# cfa_news(context, target_chat_id)

@cfa_command_dispetcher
async def cfa_news(context, target_chat_id):
  effective_chat_id = target_chat_id
  #articles = scraper.CfaAllNewsScraper(error='ignore').fetch_and_parse(period=scraper.Periods.LAST_24_HOURS)
  #articles = postgres_client.get_last_24h_news()
  articles = postgres_client.get_n_news()
  if len(articles) == 0:
    await context.bot.send_message(
      chat_id=effective_chat_id,
      text='Новости ЦФА не найдены.',
    )
    return
  post = Post(post_items=articles)
  context.bot_data['post_cache'][post.post_id] = post
  msg_text, keyboard = get_cfa_last_news_post_markup(post)
  await context.bot.send_message(
    chat_id=effective_chat_id,
    text=msg_text,
    reply_markup=keyboard,
    parse_mode=ParseMode.HTML,
    disable_web_page_preview=True,
  )

async def cfa_last_news_button_callback(update, context):
  query = update.callback_query
  btn_name = query.data
  keyboard_action, post_id = btn_name.replace(CFA_LAST_NEWS_CALLBACK_ID + '_', '').split('_')
  post = context.bot_data['post_cache'].get(post_id)
  if post is None:
    await context.bot.send_message(
      chat_id=query.message.chat.id,
      reply_to_message_id=query.message.message_id,
      text='По некоторым причинам кеш этого поста не найден, поэтому действие недоступно.'
    )
    return
  if post.pages_count == 1:
    return
  match keyboard_action:
    case 'counter':
      return
    case 'forward':
      post.next_page()
    case 'backward':
      post.previous_page()
  msg_text, keyboard = get_cfa_last_news_post_markup(post)
  await query.edit_message_text(
    text=msg_text,
    reply_markup=keyboard,
    parse_mode=ParseMode.HTML,
    disable_web_page_preview=True,
  )
