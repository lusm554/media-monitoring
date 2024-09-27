from urllib.parse import urlsplit, urlunsplit

class Article:
  '''
  Класс представление новостной статьи.
  Описывает характеристики новости - заголовок, ссылка на новость источника, время, источник и парсер статьи.
  '''
  __slots__ = ('title', 'url', 'publish_time', 'publisher_name', 'scraper', 'db_id', 'body_text', 'summarized_body_text', '_filter_url')
  def __init__(
    self, title, url, publish_time, publisher_name, scraper,
    db_id=None, body_text=None, summarized_body_text=None
  ):
    self.title = title
    self.url = url
    self.publish_time = publish_time
    self.publisher_name = publisher_name
    self.scraper = scraper
    self.db_id = db_id
    self.body_text = body_text
    self.summarized_body_text = summarized_body_text
    self._filter_url = urlunsplit(urlsplit(self.url)._replace(query="", fragment=""))

  @classmethod
  def from_dict(cls, dct):
    '''
    Constructor from dict
    '''
    self = cls(
      title=dct['title'],
      url=dct['url'],
      publish_time=dct['publish_time'],
      publisher_name=dct['publisher_name'],
      scraper=dct['scraper'],
      db_id=dct.get('db_id'),
      body_text=dct.get('body_text'),
      summarized_body_text=dct.get('summarized_body_text'),
    )
    return self

  def to_dict(self):
    '''
    Convert class example to dict
    '''
    dct = {attr: getattr(self, attr) for attr in self.__slots__}
    return dct

  def __getitem__(self, key):
    '''
    For dict unpacking operator **
    '''
    return getattr(self, key)

  def keys(self):
    '''
    For dict unpacking operator **
    '''
    return self.__slots__

  def __eq__(self, other):
    '''
    Метод сравнения двух экземпляров статьи на равенство. Статьи сравниваются по url'у.
    Приминяется при вызове оператора сравнения "==".
    '''
    if not isinstance(other, self.__class__):
      raise ValueError(f'Cannot compare instance {other!r} of different class') 
    #return self.url == other.url
    return self._filter_url == other._filter_url

  def __ne__(self, other):
    '''
    Метод сравнения двух экземпляров статьи на неравенство. Статьи сравниваются по url'у.
    Приминяется при вызове оператора сравнения "!=".
    '''
    if not isinstance(other, self.__class__):
      raise ValueError(f'Cannot compare instance {other!r} of different class') 
    #return self.url != other.url
    return self._filter_url != other._filter_url

  def __hash__(self):
    '''
    Метод хеша экземпляра класса. Возвращает хеш url'a статьи.
    Метод добавлен для удобного фильтра уникальных статей через set().
    '''
    #return hash(self.url)
    return hash(self._filter_url)

  def __repr__(self):
    '''
    Возвращает текстовое представление объекта, с помошью которого можно воссоздать объект.
    '''
    items = [ (attr, getattr(self, attr)) for attr in self.__slots__ ]
    return f'{self.__class__.__name__}(\n{",\n".join(f"{k}={v!r}"  for k,v in items)}\n)'

if __name__ == '__main__':
  dct = {'title': 1, 'url': 2, 'publish_time': 3, 'publisher_name': 4, 'scraper': 5}
  d = Article.from_dict(dct)
  print(d)
  r = d.to_dict()
  print(r)
  def test(*a, **b): print(a, b)
  test(**d)
