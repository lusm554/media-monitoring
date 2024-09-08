from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram import Update
from telegram.ext import CallbackContext
import storage
import scraper_lib as scraper
import nlp
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

'''
1. Split pages by max length 4096
2. Summarize article text up to 500 symbols
'''

def get_cfa_last_news_post_markup(post):
  msg = '\n\n'.join(
    f'{n}. <a href="{article.url}"> {article.title} </a>\n'
    f'<b>Источник:</b> {article.scraper.capitalize()}/{article.publisher_name}.\n'
    f'<b>Опубликовано:</b> {article.publish_time.strftime("%a, %d %b в %H:%M")}.\n'
    f'<blockquote expandable>{nlp.lsa_summarizer(article.body_text, sentences=2)}</blockquote>'
    for n, article in enumerate(
      post.current_page(),
      start=(post.current_page_number - 1) * post.items_count_on_page + 1
    )
    # 4096
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
async def cfa_news(context, target_chat_id):
  effective_chat_id = target_chat_id
  #articles = storage.get_last_24h_news()
  articles = storage.get_n_news(n=15)
  _r = [{a.url: a.body_text} for a in articles]
  print(_r)
  if len(articles) == 0:
    await context.bot.send_message(
      chat_id=effective_chat_id,
      text='Новости ЦФА не найдены.',
    )
    return
  post = Post(post_items=articles, page_items_cnt=3)
  # Save post to cache
  #context.bot_data['post_cache'][post.post_id] = post # bot cache
  storage.redis_client.set_complex_obj(post.post_id, post) # redis cache
  # Save post to db
  storage.add_news_posts([{'bot_post_id': post.post_id, 'news_id': art.db_id} for art in articles])
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
  # Get post from cache
  #post = context.bot_data['post_cache'].get(post_id) # bot cache
  post = storage.redis_client.get_complex_obj(post_id) # redis cache
  if post is None:
    post_articles = storage.get_articles_by_news_post(post_id)
    if len(post_articles) == 0:
      await context.bot.send_message(
        chat_id=query.message.chat.id,
        reply_to_message_id=query.message.message_id,
        text='По некоторым причинам кеш этого поста не найден, поэтому действие недоступно.'
      )
      return
    post = Post(post_items=post_articles, post_id=post_id, page_items_cnt=3)
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
  msg_text, keyboard = get_cfa_last_news_post_markup(post)
  await query.edit_message_text(
    text=msg_text,
    reply_markup=keyboard,
    parse_mode=ParseMode.HTML,
    disable_web_page_preview=True,
  )
