class RSSFeed:
  def __init__(self, title, rss_url, feed_name=None):
    self.title = title
    self.rss_url = rss_url
    self.feed_name = feed_name

  def __repr__(self):
    return f'{self.__class__.__name__}(title={self.title!r}, feed_name={self.feed_name!r}, rss_url={self.rss_url!r}'
