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
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
  ApplicationBuilder,
  MessageHandler,
  ContextTypes,
  CommandHandler,
  TypeHandler,
  CallbackQueryHandler,
  filters,
)
import scraper
from timezone import time_zone_msk
from uuid import uuid4
from collections import namedtuple

DEVELOPER_CHAT_ID = os.environ.get('DEVELOPER_CHAT_ID')

async def start(update, context):
  await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text=f'Привет! Этот бот собирает публикации СМИ по ЦФА.\n'
         f'Более подробно через команду {context.bot_data.get("cmd").help.cmd}.',
  )

async def unknown(update, context):
  await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text='Эта команда мне не знакома'
  )

async def help_cmd(update, context):
  help_msg = '\n'.join(
    f'{c.cmd} - {c.desc}'
    for c in sorted(
      [getattr(context.bot_data.get("cmd"), field) for field in context.bot_data.get("cmd")._fields],
      key=lambda x: x.ord
    )
  )
  await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text=help_msg
  )

def is_cache_expire(context):
  if (datetime.datetime.now() - context.bot_data['news_cache']['timestamp']).seconds // 60 > 10:
    logger.info(f"Cache date {context.bot_data['news_cache']['timestamp']} expire")
    return True
  return False

async def _cfa_info(context, target_chat_id):
  target_msg = await context.bot.send_message(
    chat_id=target_chat_id,
    text='Ищем новости, это займет немного времени...',
    disable_web_page_preview=True,
  )
  if context.bot_data.get('news_cache', None) is None or is_cache_expire(context):
    cfa_markup = [
      'За последнее время были опубликованы следующие новости:',
    ]
    news = context.bot_data.get('scraper').get_articles()
    news = news * 6 # REMOVE REMOVE REMOVE REMOVE REMOVE
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
      cfa_markup.append(article_markup)
    logger.info(f'Updating cache')
    context.bot_data['news_cache'] = {
      'markup': cfa_markup,
      'timestamp': datetime.datetime.now(),
    }
  else:
    logger.info(f"Return message from cache on {context.bot_data['news_cache']['timestamp']}")
    cfa_markup = context.bot_data.get('news_cache')['markup']

  '''
  pagination_keyboard = [
    [
      InlineKeyboardButton('prev', callback_data='backward'),
      InlineKeyboardButton('1/2', callback_data='counter'),
      InlineKeyboardButton('next', callback_data='forward')
    ],
  ]
  keyboard_markup = InlineKeyboardMarkup(pagination_keyboard)
  '''

  batched_markup = [cfa_markup[i:i + 15] for i in range(0, len(cfa_markup), 15)]
  for msg_markup in batched_markup:
    _makrup = '\n\n'.join(msg_markup)
    await context.bot.send_message(
      chat_id=target_chat_id,
      text=_makrup,
      parse_mode=ParseMode.HTML,
      disable_web_page_preview=True,
    )
    '''
    await context.bot.edit_message_text(
      message_id=target_msg.message_id,
      chat_id=target_chat_id,
      text=_makrup,
      parse_mode=ParseMode.HTML,
      disable_web_page_preview=True,
      reply_markup=keyboard_markup,
    )
    '''
    #break # REMOVE REMOVE REMOVE REMOVE REMOVE REMOVE

async def button(update, context):
  query = update.callback_query
  await query.answer()
  selected_button = query.data
  await query.edit_message_text(text=f"Selected option: {query.data}")

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

async def media_index(update, context):
  mindex_msg = [
    'Список отслеживаемых СМИ через RSS:',
  ]
  mindex = context.bot_data.get('scraper').get_rss_media_index() 
  for n, f in enumerate(mindex, start=1):
    msg = f'{n}. {f.title} ' + (f.feed_name or '').lower()
    mindex_msg.append(msg)
  mindex_msg.extend((
    f'\n<b>Список источников google не определен. Цель этого метода - максимизировать покрытие медиапространства ботом.</b>',
    f'\nДля фильтрации источников используется черный список - {context.bot_data.get("cmd").media_blacklist.cmd}.',
  ))
  mindex_msg = '\n'.join(mindex_msg)
  await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text=mindex_msg,
    parse_mode=ParseMode.HTML
  )

async def media_blacklist(update, context):
  msg = [
    'Список СМИ, которые входят в blacklist:',
  ]
  blacklist = context.bot_data.get('scraper').get_media_blacklist() 
  for n, i in enumerate(blacklist, start=1):
    _msg = f'{n}. {i} '
    msg.append(_msg)
  msg.append(
    '\n<b>Список распространяется на все способы получения новостей (rss, google).</b>',
  )
  markup = '\n'.join(msg)
  await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text=markup,
    parse_mode=ParseMode.HTML
  )

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
  # Add cache
  app.bot_data['news_cache'] = None
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
