import datetime
import logging

logger = logging.getLogger(__name__)

class ScraperMemCache:
  def __init__(self, items, cache_key, expire_delta=datetime.timedelta(minutes=15)):
    self.items = items
    self.cache_key = cache_key
    self.creation_time = datetime.datetime.now()
    self.expire_time = self.creation_time + expire_delta

  def is_expired(self):
    return datetime.datetime.now() > self.expire_time 

def get_articles(context, scraper, period):
  cache_key = f'{scraper}_{period}'
  scraper_cache = context.bot_data.get('scraper_cache', dict())
  scraper_result_cache = scraper_cache.get(cache_key)
  if scraper_result_cache is None or scraper_result_cache.is_expired():
    logger.info(f'Updating cache for {cache_key!r}')
    scraper_result = scraper(error='ignore').fetch_and_parse(period)
    scraper_result_cache = ScraperMemCache(
      items=scraper_result,
      cache_key=cache_key,
      expire_delta=datetime.timedelta(minutes=20)
    )
    scraper_cache[cache_key] = scraper_result_cache
  else:
    logger.info(f'Get {cache_key!r} from cache')
  scraper_result = scraper_result_cache.items
  return scraper_result