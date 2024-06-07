class Release:
  '''
  Представление выпуска ЦФА.
  Описывает характеристики выпуска - платформа выпуска, заголовок, ссылка на выпуск источника, время.
  '''
  __slots__ = ('platform_name', 'url', 'release_time', 'title')
  def __init__(self, platform_name, url, release_time, title):
    self.platform_name = platform_name
    self.url = url
    self.release_time = release_time
    self.title = title

  def __eq__(self, other):
    '''
    Метод сравнения двух экземпляров выпуска на равенство. Статьи сравниваются по url'у.
    Приминяется при вызове оператора сравнения "==".
    '''
    if not isinstance(other, self.__class__):
      raise ValueError(f'Cannot compare instance {other!r} of different class')
    return self.url == other.url

  def __ne__(self, other):
    '''
    Метод сравнения двух экземпляров выпуска на неравенство. Статьи сравниваются по url'у.
    Приминяется при вызове оператора сравнения "!=".
    '''
    if not isinstance(other, self.__class__):
      raise ValueError(f'Cannot compare instance {other!r} of different class')
    return self.url != other.url

  def __hash__(self):
    '''
    Метод хеша экземпляра класса. Возвращает хеш url'a выпуска.
    Метод добавлен для удобного фильтра уникальных выпусков через set().
    '''
    return hash(self.url)

  def __repr__(self):
    '''
    Возвращает текстовое представление объекта, с помошью которого можно воссоздать объект.
    '''
    items = [ (attr, getattr(self, attr)) for attr in self.__slots__ ]
    return f'{self.__class__.__name__}(\n{",\n".join(f"{k}={v!r}"  for k,v in items)}\n)'