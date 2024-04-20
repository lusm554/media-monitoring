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
    return f'{self.__class__.__name__}(\n{",\n".join(f"{k}={v!r}"  for k,v in items)}\n)'
