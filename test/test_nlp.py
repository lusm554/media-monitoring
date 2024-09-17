import sys; sys.path.insert(0, '.')
import nlp
import scraper_lib as scraper

def test_news_summarization():
  #news = scraper.CfaAllNewsScraper(error='raise').fetch_and_parse(period=scraper.Periods.LAST_24_HOURS)
  news = scraper.CfaAllNewsScraper(error='raise').fetch_and_parse(period=scraper.Periods.LAST_WEEK)
  print(len(news))

  for n in news:
    print(n.title, n.url)
    if n.body_text:
      print(nlp.news_text_summarization(n.body_text))
    else:
      print(n.body_text)
    print()
    print()
#test_news_summarization()

def test_release_ner():
  #releases = scraper.CfaReleasesScraper(error='raise').fetch_and_parse(period=scraper.Periods.ALL_AVAILABLE_TIME)
  releases = scraper.CfaReleasesScraper(error='raise').fetch_and_parse(period=scraper.Periods.LAST_WEEK, add_pdf_text=True)
  for r in releases:
    print(r.title)
    if r.pdf_text:
      release_desc = nlp.release_text_to_desc(r.pdf_text)
      print(release_desc)
    print()
    print()
test_release_ner()

