import bot
import storage
import os

import locale
locale.setlocale(
  category=locale.LC_ALL,
  locale='ru_RU.UTF-8',
)

import datetime
import logging
logging.basicConfig(
  level=logging.INFO,
  format='[%(asctime)s] %(levelname)s [%(name)s] %(message)s',
  datefmt='%Y-%m-%d %H:%M:%S %Z',
  handlers=[
    #logging.FileHandler(datetime.datetime.now().strftime('shared/logs/log_%Y-%m-%d_%H-%M-%S.log')),
    logging.StreamHandler(),
  ],
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

storage.create_tables_if_not_exists()
#storage.recreate_tables()

if os.getenv('BOT_NEWS_SUBSCRIBERS', ''):
  env_subscribers = [u for u in os.getenv('BOT_NEWS_SUBSCRIBERS', '').split(',') if u]
  logger.info(f'Added news subscribers from env: {env_subscribers}')
  now = datetime.datetime.now()
  storage.add_news_subscriber([{'add_time': now, 'telegram_user_id': uid} for uid in env_subscribers])

BOT_TOKEN = os.getenv('BOT_TOKEN')
USERS_BLACKLIST = os.getenv('BOT_USERS_BLACKLIST', '').split(',')
assert BOT_TOKEN
bot.start(BOT_TOKEN, USERS_BLACKLIST)
