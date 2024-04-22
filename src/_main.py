from timezone import time_zone_msk
import logging
import datetime
# setting logger timezone
logging.Formatter.converter = lambda *args: datetime.datetime.now(tz=time_zone_msk).timetuple()
logging.basicConfig(
  level=logging.INFO,
  format='[%(asctime)s] %(levelname)s [%(name)-24s] %(message)s',
  datefmt='%Y-%m-%d %H:%M:%S %Z',
  handlers=[
    logging.FileHandler(datetime.datetime.now().strftime('logs/log_%Y-%m-%d_%H-%M-%S.log')),
    logging.StreamHandler(),
  ]
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

import os; from env import set_env_vars; set_env_vars(filepath='.env')
from collections import namedtuple
import traceback, json, html
from telegram import Update
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
from commands import (
  start,
  unknown,
  help_cmd,
  media_blacklist,
  media_index,
  set_sheduler_cfa_info,
  unset_sheduler_cfa_info,
  cfa_info,
  _cfa_info,
  cfa_info_all_news,
  cfa_info_button_callback,
  cfa_emits,
  cfa_emits_button_callback
)

async def callback_cfa_info_scheduler(context):
  for chat_id in context.bot_data.get('news_scheduled_chats'):
    logger.info(f'Sending scheduled news for {chat_id}')
    await _cfa_info(context, target_chat_id=chat_id)

async def callback_cfa_info_cache_collerctor(context):
  logger.info('Check for expire posts cache')
  for internal_post_id, post in list(context.bot_data.get('post_cache').items()):
    if (datetime.datetime.now() - post['timestamp']).seconds // 3600 > 12:
      logger.info(f'Deleting post: id {internal_post_id!r}')
      del context.bot_data['post_cache'][internal_post_id]

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
    chat_id=context.bot_data.get('DEVELOPER_CHAT_ID'), text=message, parse_mode=ParseMode.HTML
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
    #logger.info(f'Update: {update!r}')
    logger.info(f'Update id: {update.update_id!r}')

async def button_callback_gateway(update, context):
  query = update.callback_query
  await query.answer()
  btn_data = query.data
  if btn_data.startswith('forward') or btn_data.startswith('backward') or btn_data.startswith('counter'):
    await cfa_info_button_callback(update, context, query, btn_data)
  if btn_data.startswith('emits'):
    await cfa_emits_button_callback(update, context, query, btn_data)
 
def main():
  Cmd = namedtuple('Cmd', ['cmd', 'desc', 'name', 'ord'])
  _cmds = (
    Cmd(cmd='/help', desc='получить инфо по командам', name='help', ord=1),
    Cmd(cmd='/start', desc='начать работу', name='start', ord=2),
    Cmd(cmd='/last_news', desc='посмотреть последние новости ЦФА', name='last_news', ord=3),
    Cmd(cmd='/emits', desc='посмотреть выпуски ЦФА', name='emits', ord=3),
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
  DEVELOPER_CHAT_ID = os.environ.get('DEVELOPER_CHAT_ID')
  logger.info(f'News scheduler init for {NEWS_SCHEDULED_CHATS}')

  app = ApplicationBuilder().token(TOKEN).build() 

  # Add dev chat id
  app.bot_data['DEVELOPER_CHAT_ID'] = DEVELOPER_CHAT_ID
  # Add description of commands
  app.bot_data['cmd'] = COMMANDS
  # Bot timezone
  app.bot_data['timezone'] = time_zone_msk
  # Add news scraper
  app.bot_data['scraper'] = scraper.get_scraper_instance(
    rss_scrp=scraper.RSS,
    dzen_scrp=scraper.DzenScraper,
    go_scrp=scraper.GoogleScraper,
    article_wrp=scraper.WrappedArticle
  )
  # Add cache for last news
  app.bot_data['news_cache'] = None
  # Add cache for news post/msg 
  app.bot_data['post_cache'] = dict()
  app.bot_data['emits_cache'] = None
  # Add chat ids for scheduled news
  app.bot_data['news_scheduled_chats'] = NEWS_SCHEDULED_CHATS
  app.bot_data['news_scheduled_time'] = datetime.time(hour=9, tzinfo=app.bot_data.get('timezone'))

  # Add job of sending news into sheduler
  #app.job_queue.run_repeating(callback_cfa_info_scheduler, interval=60, first=60) # for test command
  app.job_queue.run_daily(callback=callback_cfa_info_scheduler, time=app.bot_data.get('news_scheduled_time'))

  # Add job of collecting expired posts cache 
  app.job_queue.run_repeating(callback_cfa_info_cache_collerctor, interval=60*60*1, first=40)

  # Logger
  app.add_handler(TypeHandler(Update, updates_logger), -1)

  # Register commands
  app.add_handler(CommandHandler(COMMANDS.start.name, start))
  app.add_handler(CommandHandler(COMMANDS.help.name, help_cmd))
  app.add_handler(CommandHandler(COMMANDS.last_news.name, cfa_info))
  app.add_handler(CommandHandler('all_news', cfa_info_all_news)) # REMOVE
  app.add_handler(CommandHandler(COMMANDS.media_index.name, media_index))
  app.add_handler(CommandHandler(COMMANDS.media_blacklist.name, media_blacklist))
  app.add_handler(CommandHandler(COMMANDS.set_news_schedule.name, set_sheduler_cfa_info))
  app.add_handler(CommandHandler(COMMANDS.unset_news_schedule.name, unset_sheduler_cfa_info))
  app.add_handler(CallbackQueryHandler(button_callback_gateway)) # handler for paggination buttons 
  app.add_handler(CommandHandler(COMMANDS.emits.name, cfa_emits))

  # Unknown cmd handler
  app.add_handler(MessageHandler(filters.COMMAND, unknown))

  # Error handler
  app.add_error_handler(error_handler)

  # Run until Ctrl-C
  app.run_polling()

if __name__ == '__main__':
  main()
