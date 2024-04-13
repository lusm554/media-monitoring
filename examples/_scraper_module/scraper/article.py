class Article:
  __slots__ = ('title', 'url', 'publish_time', 'publisher_name', 'scraper')
  def __init__(self, title, url, publish_time, publisher_name, scraper):
    self.title = title
    self.url = url
    self.publish_time = publish_time
    self.publisher_name = publisher_name
    self.scraper = scraper

  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      raise ValueError(f'Cannot compare instance {other!r} of different class') 
    return self.url == other.url

  def __ne__(self, other):
    if not isinstance(other, self.__class__):
      raise ValueError(f'Cannot compare instance {other!r} of different class') 
    return self.url != other.url

  def __hash__(self):
    return hash(id(self))

  def __repr__(self):
    items = [ (attr, getattr(self, attr)) for attr in self.__slots__ ]
    return f'{self.__class__.__name__}({", ".join(f"{k}={v!r}"  for k,v in items)})'

class WrappedArticle:
  __slots__ = ('article', 'comparison_key')
  def __init__(self, article):
    self.comparison_key = 'url'
    self.article = article

  def __eq__(self, other):
    return self.article == other.article

  def __hash__(self):
    return hash(getattr(self.article, self.comparison_key))

  def __repr__(self):
    return self.article.__repr__()