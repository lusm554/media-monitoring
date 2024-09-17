class Release:
  '''
  Представление выпуска ЦФА.
  Описывает характеристики выпуска - платформа выпуска, заголовок, ссылка на выпуск источника, время.
  '''
  __slots__ = (
    'platform_name', 'url', 'release_time', 'title', 'db_id', 'pdf_text',
    'cfa_count', 'cfa_price', 'coupon_period', 'date_time_placement_start',
    'date_time_placement_end',
    'cfa_repayment_date_time',
    'cfa_repayment_method',
  )
  def __init__(
    self, platform_name, url, release_time, title, db_id=None, pdf_text=None,
    cfa_count=None, cfa_price=None, coupon_period=None, date_time_placement_start=None,
    date_time_placement_end=None,
    cfa_repayment_date_time=None,
    cfa_repayment_method=None
  ):
    self.platform_name = platform_name
    self.url = url
    self.release_time = release_time
    self.title = title
    self.db_id = db_id
    self.pdf_text = pdf_text
    self.cfa_count = cfa_count
    self.cfa_price = cfa_price
    self.coupon_period = coupon_period
    self.date_time_placement_start = date_time_placement_start
    self.date_time_placement_end = date_time_placement_end
    self.cfa_repayment_date_time = cfa_repayment_date_time
    self.cfa_repayment_method = cfa_repayment_method

  @classmethod
  def from_dict(cls, dct):
    '''
    Constructor from dict
    '''
    self = cls(**dct)
    return self

  def to_dict(self):
    '''
    Convert class example to dict
    '''
    dct = {attr: getattr(self, attr) for attr in self.__slots__}
    return dct

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
    return f'{self.__class__.__name__}(\n{",\n".join(f"{k}={v!r}" for k,v in items)}\n)'
