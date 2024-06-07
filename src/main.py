'''
Process:
Command -> Cache exist     -> Create Post & Save -> markup, buttons -> Return Result
        -> Cache not exist -> Run scraper -> Save Cache -> Create Post & Save -> markup, buttons -> Return Result

class Cache:
  Params:
    - id
    - cache_data
    - creatime_time
    - expire_time
  Methods:
    - is_expired

class Post:
  Params:
    - id

  class CfaNewsPost:
    Params:
      - data
      ...
    Methods:
      - button callback
      - post markup generator

  class CfaReleasesPost:
    ...

class ScraperResult:
  Params:
    - id
    - scraper_result

Scenarios:
  Scraper -> ScraperResult -> Cache
  ScraperResult -> Post -> Cache

  !But why, if we can!:
    Scraper -> ScraperResult -> Post -> Cache

class ScraperCommandFactory:
  pass 
'''
from timezone import time_zone_moscow
import datetime
import logging

logging.Formatter.converter = lambda *args: datetime.datetime.now(tz=time_zone_moscow).timetuple()
logging.basicConfig(
  level=logging.INFO,
  format='[%(asctime)s] %(levelname)s [%(name)s] %(message)s',
  datefmt='%Y-%m-%d %H:%M:%S %Z',
  handlers=[
    logging.FileHandler(datetime.datetime.now().strftime('logs/log_%Y-%m-%d_%H-%M-%S.log')),
    logging.StreamHandler(),
  ],
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

from telegram import Update, BotCommand
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
import os
from collections import namedtuple
import asyncio
from env import set_env_vars
import bot_commands
import bot_handlers
import bot_regular_tasks
import scraper

def setup_bot_data_variables(telegram_app, commands):
  telegram_app.bot_data['commands'] = commands
  telegram_app.bot_data['scraper'] = scraper
  telegram_app.bot_data['post_cache'] = dict()
  telegram_app.bot_data['scraper_cache'] = dict()
  telegram_app.bot_data['regular_newsletter_chats'] = set(str(x) for x in os.environ.get('NEWS_SCHEDULED_CHATS').split(',') if x != '')
  telegram_app.bot_data['bot_timezone'] = time_zone_moscow
  telegram_app.bot_data['cfa_newsletter_time'] = datetime.time(hour=9, tzinfo=time_zone_moscow)
  telegram_app.bot_data['cfa_releases_time'] = datetime.time(hour=19, tzinfo=time_zone_moscow)
  telegram_app.bot_data['DEVELOPER_CHAT_ID'] = os.environ.get('DEVELOPER_CHAT_ID')

def setup_bot_handlers(telegram_app, commands):
  telegram_app.add_handler(TypeHandler(Update, bot_handlers.updates_logger), -1)
  for command in commands:
    telegram_app.add_handler(
      CommandHandler(
        command=command.name,
        callback=command.callback
      )
    )
  telegram_app.add_handler(
    CallbackQueryHandler(
      bot_handlers.button_dispatcher({
        'cfa_last_news': bot_commands.cfa_last_news_button_callback,
        'cfa_releases': bot_commands.cfa_releases_button_callback,
      })
    )
  )
  telegram_app.add_handler(MessageHandler(filters.COMMAND, bot_handlers.unknown))
  telegram_app.add_error_handler(bot_handlers.error_handler)

def shedule_bot_tasks(telegram_app):
  job_interval = datetime.timedelta(hours=1)
  job_time_to_first_run = datetime.timedelta(seconds=30)
  newsletter_time = telegram_app.bot_data.get('cfa_newsletter_time')
  releases_time = telegram_app.bot_data.get('cfa_releases_time')
  telegram_app.job_queue.run_repeating(
    callback=bot_regular_tasks.post_cache_cleaner,
    interval=job_interval,
    first=job_time_to_first_run,
  )
  telegram_app.job_queue.run_daily(
    callback=bot_regular_tasks.cfa_news_sender,
    time=newsletter_time,
    data=bot_commands.cfa_last_news_regular,
  )
  telegram_app.job_queue.run_daily(
    callback=bot_regular_tasks.cfa_releases_sender,
    time=releases_time,
    data=bot_commands.cfa_last_releases_regular,
  )
  # telegram_app.job_queue.run_repeating(
  #   bot_regular_tasks.cfa_news_sender,
  #   interval=60,
  #   first=15,
  #   data=bot_commands.cfa_last_releases_regular,
  # )

def set_list_of_bot_commands(telegram_app, commands):
  cmds = [
    BotCommand(command=cmd.name, description=cmd.desc)
    for cmd in commands
  ]
  loop = asyncio.get_event_loop()
  loop.run_until_complete(telegram_app.bot.set_my_commands(cmds))

def main():
  set_env_vars(filepath='./.env')
  Command = namedtuple('Cmd', ['callback', 'desc', 'name'])
  commands = (
    Command(callback=bot_commands.start, desc='начать работу', name='start'),
    Command(callback=bot_commands.help_, desc='инфо по командам', name='help'),
    Command(callback=bot_commands.cfa_last_news, desc='новости ЦФА за сутки', name='last_news_cfa'),
    Command(callback=bot_commands.cfa_week_news, desc='новости ЦФА за неделю', name='week_news_cfa'),
    Command(callback=bot_commands.cfa_last_releases, desc='выпуски ЦФА за сутки', name='last_releases_cfa'),
    Command(callback=bot_commands.cfa_week_releases, desc='выпуски ЦФА за неделю', name='week_releases_cfa'),
    Command(callback=bot_commands.cfa_all_time_releases, desc='выпуски ЦФА за все время', name='all_releases_cfa'),
    Command(callback=bot_commands.newsletter_subscribe, desc='рассылка новостей ЦФА', name='subscribe_news'),
    Command(callback=bot_commands.newsletter_cancel_subscribe, desc='отменить рассылку новостей ЦФА', name='cancel_subscribe_news'),
  )
  if os.environ.get('dev'):
    TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN_DEV')
    logger.info(f'Run with DEV token {TELEGRAM_TOKEN!r}')
  else:
    TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
    logger.info(f'Run with PROM token {TELEGRAM_TOKEN!r}')
  telegram_app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
  setup_bot_data_variables(telegram_app, commands)
  setup_bot_handlers(telegram_app, commands)
  shedule_bot_tasks(telegram_app)
  set_list_of_bot_commands(telegram_app, commands)
  telegram_app.run_polling()

if __name__ == '__main__':
  main()
  # import asyncio
  # asyncio.run(main())