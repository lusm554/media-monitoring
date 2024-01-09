class PaginationPointer:
  def __init__(self, size, current=0):
    assert current >= 0 and current <= size 
    self.size = size
    self.current = current

  def forward(self):
    if self.current == self.size:
      self.current = 0
    else:
      self.current += 1
    return self.current

  def backward(self):
    if self.current == 0:
      self.current = self.size
    else:
      self.current -= 1
    return self.current

  def __repr__(self):
    return f'{self.__class__.__name__}({", ".join(f"{k}={v!r}" for k,v in self.__dict__.items())})'

if __name__ == '__main__':
  ''' 
  a = list(f'a{i}' for i in range(5))
  p = PaginationPointer(size=len(a)-1)
  print(a)
  for i in range(10):
    print(i, a[p.forward()], p)

  p = PaginationPointer(size=len(a)-1)
  print(a)
  for i in range(10):
    print(i, a[p.backward()], p)

  print()
  ''' 
  p = PaginationPointer(size=0)
  print(p)
  p.forward()
  print(p)
  p.backward()
  print(p)
