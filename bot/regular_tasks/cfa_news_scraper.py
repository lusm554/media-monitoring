import scraper_lib
import storage
import nlp

async def cfa_news_scraper(context):
  def get_news_not_in_db(scraper_news):
    scraper_news_in_db = storage.get_news([c.url for c in scraper_news])
    scraper_news_in_db_urls = {t['url'] for t in scraper_news_in_db}
    scraper_news_not_in_db = [r for r in scraper_news if r.url not in scraper_news_in_db_urls]
    return scraper_news_not_in_db

  articles = scraper_lib.CfaAllNewsScraper(error='ignore').fetch_and_parse(period=scraper_lib.Periods.LAST_WEEK)
  print('scraper news', len(articles))
  acticles_not_in_db = get_news_not_in_db(articles) # 1. Get news not in db
  print('news no in db', len(acticles_not_in_db))

  for a in acticles_not_in_db:
    if a.body_text is None: continue
    news_sum = nlp.news_text_summarization(a.body_text)
    setattr(a, 'summarized_body_text', news_sum)
  storage.add_news(acticles_not_in_db)

async def cfa_releases_scraper(context):
  def get_releases_not_in_db(scraper_releases):
    scraper_releases_in_db = storage.get_releases([c.url for c in scraper_releases])
    scraper_releases_in_db_urls = {t['url'] for t in scraper_releases_in_db}
    scraper_releases_not_in_db = [r for r in scraper_releases if r.url not in scraper_releases_in_db_urls]
    return scraper_releases_not_in_db

  releases_scraper = scraper_lib.CfaReleasesScraper(error='ignore')
  releases = releases_scraper.fetch_and_parse(scraper_lib.Periods.LAST_WEEK) # scraper_lib.Periods.LAST_24_HOURS
  #releases = sorted(releases, key=lambda x: x.url)[:1]
  print('scraper releases', len(releases))
  releases = get_releases_not_in_db(releases) # 1. Get releases not in db
  print('not in db releases', len(releases))
  releases = [releases_scraper.add_pdf_text(r) for r in releases] # 2. Get pdf, convert to text
  for r in releases:
    desc = nlp.release_text_to_desc(r.pdf_text) # 3. Pdf text ner
    for k,v in desc.items():
      setattr(r, k, v)
  storage.add_releases(releases)

