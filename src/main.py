import logging
import datetime
logging.basicConfig(
  level=logging.INFO,
  format='[%(asctime)s] %(levelname)s [%(name)-24s] %(message)s',
  datefmt='%Y-%m-%d %H:%M:%S',
  handlers=[
    logging.FileHandler(datetime.datetime.now().strftime('logs/log_%Y-%m-%d_%H-%M-%S.log')),
    logging.StreamHandler(),
  ]
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

import os; from env import set_env_vars; set_env_vars(filepath='.env')
import traceback, json, html
import functools
from telegram.constants import ParseMode
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
  ApplicationBuilder,
  MessageHandler,
  ContextTypes,
  CommandHandler,
  TypeHandler,
  CallbackQueryHandler,
  filters,
)
from uuid import uuid4
from collections import namedtuple
import scraper
from timezone import time_zone_msk
from pagination_pointer import PaginationPointer

DEVELOPER_CHAT_ID = os.environ.get('DEVELOPER_CHAT_ID')

from commands import (
  start,
  unknown,
  help_cmd,
  media_blacklist,
  media_index,
)

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

async def button(update, context):
  query = update.callback_query
  await query.answer()
  btn_data = query.data
  action, internal_post_id = btn_data.split('_')
  logger.info(f'Button clicked with action {action!r}, id {internal_post_id!r}')

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

def notify_about_chat_updates(func):
  @functools.wraps(func)
  async def wrapper(update, context):
    result = await func(update, context)
    logger.info('Sending last version of chats to dev chat')
    _chats = ','.join(context.bot_data.get("news_scheduled_chats"))
    message = f'Last version of chats {_chats!r}'
    await context.bot.send_message(
      chat_id=DEVELOPER_CHAT_ID,
      text=message
    )
    return result
  return wrapper

@notify_about_chat_updates
async def set_sheduler_cfa_info(update, context):
  chat_id = str(update.effective_message.chat_id)
  try:
    context.bot_data.get('news_scheduled_chats').add(chat_id)
    logger.info(f'News scheduler chats after added new chat {context.bot_data.get("news_scheduled_chats")}')
    schedule_time_str = context.bot_data.get('news_scheduled_time').strftime(f'%H:%M {time_zone_msk}')
    msg = (
      f'Новости будут приходить в {schedule_time_str} каждый день.\n'
      f'Чтобы отменить - {context.bot_data.get("cmd").unset_news_schedule.cmd}.'
    )
    await update.effective_message.reply_text(msg)
  except Exception as error:
    raise error

@notify_about_chat_updates
async def unset_sheduler_cfa_info(update, context):
  chat_id = str(update.effective_message.chat_id)
  try:
    context.bot_data.get('news_scheduled_chats').remove(chat_id)
    logger.info(f'News scheduler chats after removed chat {context.bot_data.get("news_scheduled_chats")}')
    msg = 'Запланированные новости выключены.'
    await update.effective_message.reply_text(msg)
  except KeyError:
    error_msg = (
      f'Похоже ранее новости не планировались.\n'
      f'Воспользуйтесь {context.bot_data.get("cmd").set_news_schedule.cmd}.'
    )
    await update.effective_message.reply_text(error_msg)

async def cfa_info(update, context):
  target_chat_id = update.effective_chat.id
  await _cfa_info(context, target_chat_id=target_chat_id)

async def callback_cfa_info_scheduler(context):
  for chat_id in context.bot_data.get('news_scheduled_chats'):
    logger.info(f'Sending scheduled news for {chat_id}')
    await _cfa_info(context, target_chat_id=chat_id)

async def error_handler(update, context):
  logger.error("Exception while handling an update:", exc_info=context.error)
  tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
  tb_string = "".join(tb_list)
  update_str = update.to_dict() if isinstance(update, Update) else str(update)
  message = (
    f"An exception was raised while handling an update\n"
    f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
    f"</pre>\n\n"
    f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
    f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
    f"<pre>{html.escape(tb_string)}</pre>"
  )
  await context.bot.send_message(
    chat_id=DEVELOPER_CHAT_ID, text=message, parse_mode=ParseMode.HTML
  )

async def updates_logger(update, context):
  try:
    show_obj = {
      'user': update.message.from_user,
      'chat': update.message.chat,
      'text': update.message.text,
    }
    logger.info(f'Update: {show_obj!r}')
  except:
    logger.info(f'Update: {update!r}')

def main():
  Cmd = namedtuple('Cmd', ['cmd', 'desc', 'name', 'ord'])
  _cmds = (
    Cmd(cmd='/help', desc='получить инфо по командам', name='help', ord=1),
    Cmd(cmd='/start', desc='начать работу', name='start', ord=2),
    Cmd(cmd='/last_news', desc='посмотреть последние новости ЦФА', name='last_news', ord=3),
    Cmd(cmd='/media_index', desc='посмотреть список отслеживаемых СМИ', name='media_index', ord=4),
    Cmd(cmd='/media_blacklist', desc='посмотреть blacklist СМИ', name='media_blacklist', ord=5),
    Cmd(cmd='/set_news_schedule', desc='запланировать регулярные новости каждое утро', name='set_news_schedule', ord=6),
    Cmd(cmd='/unset_news_schedule', desc='отменить запланированные новости', name='unset_news_schedule', ord=7),
  )
  COMMANDS = namedtuple('Commands', [x.name for x in _cmds])(**{ c.name: c for c in _cmds })

  if os.environ.get('dev'):
    logger.info('Running from dev token TELEGRAM_TOKEN_DEV')
    TOKEN = os.environ.get('TELEGRAM_TOKEN_DEV')
  else:
    TOKEN = os.environ.get('TELEGRAM_TOKEN')
    logger.info('Running from prom token TELEGRAM_TOKEN')
  NEWS_SCHEDULED_CHATS = set(str(x) for x in os.environ.get('NEWS_SCHEDULED_CHATS').split(',') if x != '')
  logger.info(f'News scheduler init for {NEWS_SCHEDULED_CHATS}')

  app = ApplicationBuilder().token(TOKEN).build() 

  # Add description of commands
  app.bot_data['cmd'] = COMMANDS

  # Add news scraper
  app.bot_data['scraper'] = scraper.get_scraper_instance(
    rss_scrp=scraper.RSS,
    go_scrp=scraper.GoogleScraper,
    article_wrp=scraper.WrappedArticle
  )
  # Add cache for last news
  app.bot_data['news_cache'] = None
  # Add cache for news post/msg 
  app.bot_data['post_cache'] = dict()
  # Add chat ids for scheduled news
  app.bot_data['news_scheduled_chats'] = NEWS_SCHEDULED_CHATS
  app.bot_data['news_scheduled_time'] = datetime.time(hour=9, tzinfo=time_zone_msk)

  # Add job of sending news into sheduler
  #app.job_queue.run_repeating(callback_cfa_info_scheduler, interval=60, first=60) # for test command
  app.job_queue.run_daily(callback=callback_cfa_info_scheduler, time=app.bot_data.get('news_scheduled_time'))

  # Logger
  app.add_handler(TypeHandler(Update, updates_logger), -1)

  # Register commands
  app.add_handler(CommandHandler(COMMANDS.start.name, start))
  app.add_handler(CommandHandler(COMMANDS.help.name, help_cmd))
  app.add_handler(CommandHandler(COMMANDS.last_news.name, cfa_info))
  app.add_handler(CommandHandler(COMMANDS.media_index.name, media_index))
  app.add_handler(CommandHandler(COMMANDS.media_blacklist.name, media_blacklist))
  app.add_handler(CommandHandler(COMMANDS.set_news_schedule.name, set_sheduler_cfa_info))
  app.add_handler(CommandHandler(COMMANDS.unset_news_schedule.name, unset_sheduler_cfa_info))
  app.add_handler(CallbackQueryHandler(button)) # handler for paggination buttons 

  # Unknown cmd handler
  app.add_handler(MessageHandler(filters.COMMAND, unknown))

  # Error handler
  app.add_error_handler(error_handler)

  # Run until Ctrl-C
  app.run_polling()

if __name__ == '__main__':
  main()
