import scraper_lib
import storage

async def cfa_news_scraper(context):
  articles = scraper_lib.CfaAllNewsScraper(error='ignore').fetch_and_parse(period=scraper_lib.Periods.LAST_24_HOURS)
  storage.add_news(articles)

async def cfa_releases_scraper(context):
  #releases = scraper_lib.CfaReleasesScraper(error='ignore').fetch_and_parse(scraper_lib.Periods.LAST_24_HOURS)
  releases = scraper_lib.CfaReleasesScraper(error='ignore').fetch_and_parse(scraper_lib.Periods.LAST_WEEK)
  print(releases)
  storage.add_releases(releases)
  print(storage.get_n_releases())

