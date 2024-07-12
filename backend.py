import bot
import storage
import os

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

storage.create_tables()
#storage.recreate_tables()

'''
storage.add_news(
  [{
    'title': 'test',
    'url': 'https://google.com',
    'publish_time': datetime.datetime.now(),
    'publisher_name': 'dzen',
    'scraper': 'rss',
  }]
)

rows = storage.get_news_by_date_range(datetime.datetime.now() - datetime.timedelta(hours=24), datetime.datetime.now())
print(rows)
'''

exit()
BOT_TOKEN = os.getenv('BOT_TOKEN')
assert BOT_TOKEN
bot.start(BOT_TOKEN)
