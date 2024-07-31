from bot.regular_tasks.cfa_news_sender import cfa_news_sender

async def cfa_news_scraper(context):
  import scraper_lib
  import storage
  #articles = scraper_lib.CfaAllNewsScraper(error='ignore').fetch_and_parse(period=scraper_lib.Periods.LAST_24_HOURS)
  articles = scraper_lib.CfaGoogleNewsScraper(error='ignore').fetch_and_parse(period=scraper_lib.Periods.LAST_24_HOURS)
  print(articles)
  storage.add_news(articles)
  n = storage.get_n_news(100)
  print(n)
