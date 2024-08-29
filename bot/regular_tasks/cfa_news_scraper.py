import scraper_lib
import storage

async def cfa_news_scraper(context):
  #articles = scraper_lib.CfaAllNewsScraper(error='ignore').fetch_and_parse(period=scraper_lib.Periods.LAST_24_HOURS)
  articles = scraper_lib.CfaAllNewsScraper(error='raise').fetch_and_parse(period=scraper_lib.Periods.LAST_24_HOURS)
  storage.add_news(articles)

