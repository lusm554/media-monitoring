class RSSFeed:
  def __init__(self, title, rss_url):
    self.title = title
    self.rss_url = rss_url

  def __repr__(self):
    return f'{self.__class__.__name__}(title={self.title!r}, rss_url={self.rss_url!r}'
