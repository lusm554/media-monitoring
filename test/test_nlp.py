import sys; sys.path.insert(0, '.')
import nlp
import scraper_lib as scraper

def test_summarization():
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
test_summarization()


