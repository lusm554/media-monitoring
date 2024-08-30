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

storage.create_tables_if_not_exists()
#storage.recreate_tables()

'''
from pprint import pprint
#articles = storage.get_last_24h_news()
#pprint(articles[:3])

#post_articles = [{'bot_post_id': 'sdfsd', 'news_id': art.db_id} for art in articles]
#storage.add_news_post(post_articles)
t = storage.get_n_news_posts()
pprint(t)

t = storage.get_news_post('ad3732aa-3cda-4093-bf33-25dcbae19d8e')
pprint(t)

t = storage.get_articles_by_news_post('ad3732aa-3cda-4093-bf33-25dcbae19d8e')
pprint(t)

exit()
'''

BOT_TOKEN = os.getenv('BOT_TOKEN')
assert BOT_TOKEN
bot.start(BOT_TOKEN)
