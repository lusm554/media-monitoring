class Article:
  '''
  Класс представление новостной статьи.
  Описывает характеристики новости - заголовок, ссылка на новость источника, время, источник и парсер статьи.
  '''
  __slots__ = ('title', 'url', 'publish_time', 'publisher_name', 'scraper')
  def __init__(self, title, url, publish_time, publisher_name, scraper):
    self.title = title
    self.url = url
    self.publish_time = publish_time
    self.publisher_name = publisher_name
    self.scraper = scraper

  @classmethod
  def from_dict(cls, dct):
    self = cls(
      title=dct['title'],
      url=dct['url'],
      publish_time=dct['publish_time'],
      publisher_name=dct['publisher_name'],
      scraper=dct['scraper'],
    )
    return self

  def __eq__(self, other):
    '''
    Метод сравнения двух экземпляров статьи на равенство. Статьи сравниваются по url'у.
    Приминяется при вызове оператора сравнения "==".
    '''
    if not isinstance(other, self.__class__):
      raise ValueError(f'Cannot compare instance {other!r} of different class') 
    return self.url == other.url

  def __ne__(self, other):
    '''
    Метод сравнения двух экземпляров статьи на неравенство. Статьи сравниваются по url'у.
    Приминяется при вызове оператора сравнения "!=".
    '''
    if not isinstance(other, self.__class__):
      raise ValueError(f'Cannot compare instance {other!r} of different class') 
    return self.url != other.url

  def __hash__(self):
    '''
    Метод хеша экземпляра класса. Возвращает хеш url'a статьи.
    Метод добавлен для удобного фильтра уникальных статей через set().
    '''
    return hash(self.url)

  def __repr__(self):
    '''
    Возвращает текстовое представление объекта, с помошью которого можно воссоздать объект.
    '''
    items = [ (attr, getattr(self, attr)) for attr in self.__slots__ ]
    return f'{self.__class__.__name__}(\n{",\n".join(f"{k}={v!r}"  for k,v in items)}\n)'
