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

#storage.create_tables()
storage.recreate_tables()

from scraper_lib import Article
dct = {'title': 1, 'url': '2', 'publish_time': 3, 'publisher_name': 4, 'scraper': 5}
art = Article.from_dict(dct)
news = [art]
storage.add_news(news)
storage.add_news(news)
print(storage.get_news_by_date_range())

BOT_TOKEN = os.getenv('BOT_TOKEN')
assert BOT_TOKEN
#bot.start(BOT_TOKEN)
