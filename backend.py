import bot
import storage
import os

import locale
locale.setlocale(
  category=locale.LC_ALL,
  locale='ru_RU',
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

BOT_TOKEN = os.getenv('BOT_TOKEN')
assert BOT_TOKEN
bot.start(BOT_TOKEN)
