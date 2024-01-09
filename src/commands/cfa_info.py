import sys; sys.path.append('..'); import scraper; from pagination_pointer import PaginationPointer
from uuid import uuid4
import datetime
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode

logger = logging.getLogger(__name__)

def is_news_cache_expire(context):
  if (datetime.datetime.now() - context.bot_data['news_cache']['timestamp']).seconds // 60 > 10:
    logger.info(f"Cache date {context.bot_data['news_cache']['timestamp']} expire")
    return True
  return False

def get_pagination_markup(post_cache, page_num=0):
  page_articles = 4
  internal_post_id = post_cache['internal_post_id']
  post_markup = post_cache['markup']
  pointer = post_cache['pointer']
  current_page = '\n\n'.join(post_markup[page_num])
  pagination_keyboard = [
    [
      InlineKeyboardButton('prev', callback_data=f'backward_{internal_post_id}'),
      InlineKeyboardButton(f'{pointer.current+1}/{pointer.size+1}', callback_data=f'counter_{internal_post_id}'),
      InlineKeyboardButton('next', callback_data=f'forward_{internal_post_id}')
    ],
  ]
  keyboard_markup = InlineKeyboardMarkup(pagination_keyboard)
  return current_page, keyboard_markup

async def _cfa_info(context, target_chat_id):
  target_msg = await context.bot.send_message(
    chat_id=target_chat_id,
    text='Ищем новости, это займет немного времени...',
    disable_web_page_preview=True,
  )
  if context.bot_data.get('news_cache', None) is None or is_news_cache_expire(context):
    post_markup = [
      'За последнее время были опубликованы следующие новости:',
    ]
    #news = context.bot_data.get('scraper').get_articles()
    ################ REMOVE ##################
    news = []

    _t = scraper.Article(
      title='S2',
      url='C',
      publish_time=datetime.datetime.now(),
      publisher_name='AA:/',
      scraper='rss'
    )
    news = [_t] # REMOVE REMOVE REMOVE REMOVE REMOVE
    news = news * 13 # REMOVE REMOVE REMOVE REMOVE REMOVE
    ################ REMOVE ##################
    for n, article in enumerate(news, start=1):
      publisher = article.publisher_name
      title = article.title
      url = article.url
      publish_time = article.publish_time.strftime('%Y-%m-%d %H:%M:%S')
      scraper_type = article.scraper
      article_markup = (
        f'{n}. <a href="{url}"> {title} </a>\n'
        f'<b>Источник:</b> {publisher}.\n'
        f'<b>Опубликовано:</b> {publish_time}.\n'
        f'<b>Взято из:</b> {scraper_type}.'
      )
      post_markup.append(article_markup)
    logger.info(f'Updating cache')
    context.bot_data['news_cache'] = {
      'markup': post_markup,
      'timestamp': datetime.datetime.now(),
    }
  else:
    logger.info(f"Return message from cache on {context.bot_data['news_cache']['timestamp']}")
    post_markup = context.bot_data.get('news_cache')['markup']

  if len(post_markup) <= 1:
    await context.bot.edit_message_text(
      message_id=target_msg.message_id,
      chat_id=target_chat_id,
      text='Новости за последнее время не найдены.',
    )
    return

  internal_post_id = str(uuid4())
  post_markup_p = [post_markup[i:i + 4] for i in range(0, len(post_markup), 4)]
  logger.info(f'Saving post cache with id {internal_post_id!r}')
  context.bot_data['post_cache'][internal_post_id] = {
    'markup': post_markup_p,
    'timestamp': datetime.datetime.now(),
    'internal_post_id': internal_post_id,
    'pointer': PaginationPointer(size=len(post_markup_p)-1),
  }

  post_markup, keyboard_markup = get_pagination_markup(
    post_cache=context.bot_data['post_cache'].get(internal_post_id),
    page_num=0,
  )
  await context.bot.edit_message_text(
    message_id=target_msg.message_id,
    chat_id=target_chat_id,
    text=post_markup,
    parse_mode=ParseMode.HTML,
    disable_web_page_preview=True,
    reply_markup=keyboard_markup,
  )

async def cfa_info_button_callback(update, context):
  query = update.callback_query
  await query.answer()
  btn_data = query.data
  action, internal_post_id = btn_data.split('_')
  logger.info(f'Button clicked with action {action!r}, id {internal_post_id!r}')

  if context.bot_data['post_cache'].get(internal_post_id)['pointer'].size == 0:
    return

  if action == 'counter':
    return 
  if action == 'backward':
    context.bot_data['post_cache'].get(internal_post_id)['pointer'].backward()
  if action == 'forward':
    context.bot_data['post_cache'].get(internal_post_id)['pointer'].forward()

  post_markup, keyboard_markup = get_pagination_markup(
    post_cache=context.bot_data['post_cache'].get(internal_post_id),
    page_num=context.bot_data['post_cache'].get(internal_post_id)['pointer'].current,
  )
  await query.edit_message_text(
    text=post_markup,
    parse_mode=ParseMode.HTML,
    disable_web_page_preview=True,
    reply_markup=keyboard_markup,
  )

async def cfa_info(update, context):
  target_chat_id = update.effective_chat.id
  await _cfa_info(context, target_chat_id=target_chat_id)
