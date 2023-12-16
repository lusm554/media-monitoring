class Article:
  def __init__(self, title, url, publish_time, publisher_name):
    self.title = title
    self.url = url
    self.publish_time = publish_time
    self.publisher_name = publisher_name

  def __repr__(self):
    return f'{self.__class__.__name__}({", ".join(f"{k}={v!r}"  for k,v in self.__dict__.items())})'

if __name__ == '__main__':
  art = Article(
    title='S',
    url='C',
    publish_time='R',
    publisher_name='AA:/',
  )
  print(art)
  print(repr(art))
