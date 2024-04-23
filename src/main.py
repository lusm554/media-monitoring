'''
Commands:
  Standard:
    - help
    - start
  Specific:
    - last_news
    - emits
    - media_index
    - media_blacklist
    - set_news_schedule
    - unset_news_schedule

Functionality:
  Main:
    - cfa news
    - cfa releases
    - regular cfa news and releases
  Side:
    - show news blacklist
    - show rss media index
  
Structure:
  commands/
  scraper/
  main.py
  ...other.py

Handlers:
  1. Command
  2. buttons
  3. Updates
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
import scraper

def setup_bot_data_variables(telegram_app, commands):
  telegram_app.bot_data['commands'] = commands
  telegram_app.bot_data['scraper'] = scraper

def setup_bot_handlers(telegram_app, commands):
  telegram_app.add_handler(TypeHandler(Update, bot_handlers.updates_logger), -1)
  for command in commands:
    telegram_app.add_handler(
      CommandHandler(
        command=command.name,
        callback=command.callback
      )
    )
  telegram_app.add_handler(MessageHandler(filters.COMMAND, bot_handlers.unknown))
  telegram_app.add_error_handler(bot_handlers.error_handler)


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
  set_list_of_bot_commands(telegram_app, commands)
  telegram_app.run_polling()

if __name__ == '__main__':
  main()
  # import asyncio
  # asyncio.run(main())