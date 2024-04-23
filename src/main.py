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
import os
from env import set_env_vars

def main():
  set_env_vars(filepath='./.env')
  if os.environ.get('dev'):
    TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN_DEV')
    logger.info(f'Run with DEV token {TELEGRAM_TOKEN!r}')
  else:
    TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
    logger.info(f'Run with PROM token {TELEGRAM_TOKEN!r}')
  telegram_app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

if __name__ == '__main__':
  main()