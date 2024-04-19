from .base_scraper import NewsBaseScraper
from .article import Article
import feedparser
import logging

logger = logging.getLogger(__name__)

class RssFeed:
  def __init__(self, publisher_name, url, feed_name=None):
    self.publisher_name = publisher_name
    self.url = url
    self.feed_name = feed_name
  
  def __repr__(self):
    cls_name = self.__class__.__name__
    args = ', '.join(f'{k}={v!r}' for k,v in self.__dict__.items())
    return f'{cls_name}({args})'

class CfaRssNewsScraper(NewsBaseScraper):
  def __init__(self):
    self.RSS_FEEDS = (
      RssFeed(publisher_name='РИА Новости', url='https://ria.ru/export/rss2/archive/index.xml'),
      RssFeed(publisher_name='Рамблер', url='https://news.rambler.ru/rss/'),
      RssFeed(publisher_name='РБК', url='https://rssexport.rbc.ru/rbcnews/news/30/full.rss'),
      RssFeed(publisher_name='Новости Mail.ru', url='https://news.mail.ru/rss/90/'),
      RssFeed(publisher_name='Регнум', url='https://regnum.ru/rss'),
      RssFeed(publisher_name='ТАСС', url='https://tass.ru/rss/v2.xml'),
      RssFeed(publisher_name='Интерфакс', url='https://www.interfax.ru/rss.asp'),
      RssFeed(publisher_name='RT на русском', url='https://russian.rt.com/rss'),
      RssFeed(publisher_name='Известия', url='https://iz.ru/xml/rss/all.xml'),
      RssFeed(publisher_name='Российская газета', url='https://rg.ru/xml/index.xml'),
      RssFeed(publisher_name='Коммерсантъ', url='https://www.kommersant.ru/RSS/news.xml'),
      RssFeed(publisher_name='Ведомости', feed_name='Все новости', url='https://www.vedomosti.ru/rss/news.xml'),
      RssFeed(publisher_name='Ведомости', feed_name='Все материалы', url='https://www.vedomosti.ru/rss/articles.xml'),
      RssFeed(publisher_name='lenta.ru', url='https://lenta.ru/rss'),
      RssFeed(publisher_name='Московский Комсомолец', feed_name='Все материалы', url='https://www.mk.ru/rss/news/index.xml'),
      RssFeed(publisher_name='Московский Комсомолец', feed_name='Новостная лента', url='https://www.mk.ru/rss/news/index.xml'),
      RssFeed(publisher_name='Газета.ru', url='https://www.gazeta.ru/export/rss/social_more.xml'),
      RssFeed(publisher_name='RT', url='https://russian.rt.com/rss'),
      RssFeed(publisher_name='Финмаркет', url='http://www.finmarket.ru/rss/mainnews.asp'),
      RssFeed(publisher_name='Росбалт', url='https://www.rosbalt.ru/feed/'),
      RssFeed(publisher_name='Прайм', feed_name='Основной поток', url='https://1prime.ru/export/rss2/index.xml'),
      RssFeed(publisher_name='Прайм', feed_name='Финансы', url='https://1prime.ru/export/rss2/finance/index.xml'),
      RssFeed(publisher_name='Прайм', feed_name='Экономика', url='https://1prime.ru/export/rss2/state_regulation/index.xml'),
      RssFeed(publisher_name='Bits.media', url='https://bits.media/rss2/'),
      RssFeed(publisher_name='Indicator', url='https://indicator.ru/exports/rss'),
      RssFeed(publisher_name='Финам', feed_name='Новости компаний', url='https://www.finam.ru/analysis/conews/rsspoint/'),
      RssFeed(publisher_name='Финам', feed_name='Новости мировых рынков', url='https://www.finam.ru/international/advanced/rsspoint/'),
      RssFeed(publisher_name='Comnews', url='https://www.comnews.ru/rss'),
      RssFeed(publisher_name='tadviser.ru', url='https://www.tadviser.ru/xml/tadviser.xml'),
    )

  def feed_fetcher(self, url):
    feed_data = feedparser.parse(url)
    return feed_data

  def feed_parser(self, feed_data, article_publisher_name='Не определен'):
    articles = list()
    for entry in feed_data.entries:
      article_title = entry.get('title', '')      
      if not ('цфа' in article_title.lower() or 'цифровые финансовые активы' in article_title.lower()):
        continue
      article_url = entry.get('link')
      article_publish_time = entry.get('published_parsed')
      article = Article(
        title=article_title,
        url=article_url,
        publish_time=article_publish_time,
        publisher_name=article_publisher_name,
        scraper='rss',
      )
      articles.append(article)
    return articles

  def fetch_and_parse(self, period):
    articles = list()
    for feed in self.RSS_FEEDS:
      print(feed)
      feed_data = self.feed_fetcher(feed.url)
      cfa_articles = self.feed_parser(feed_data, feed.publisher_name)
      print(len(cfa_articles))