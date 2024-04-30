import datetime
from uuid import uuid4

class Post:
  def __init__(self, post_items, post_id=uuid4(), creation_time=None, page_items_cnt=4):
    self._items_count_on_page = page_items_cnt
    self._current_page = 0
    self.post_id = str(post_id)
    self.post_items = post_items
    self.pages = [
      self.post_items[i:i+self._items_count_on_page]
      for i in range(0, len(self.post_items), self._items_count_on_page)
    ]
    self._pages_cnt = len(self.pages) - 1
    self.creation_time = creation_time or datetime.datetime.now()

  def current_page(self):
    return self.pages[self._current_page]

  def next_page(self):
    if self._current_page == self._pages_cnt:
      self._current_page = 0
    else:
      self._current_page += 1
    return self.pages[self._current_page]

  def previous_page(self):
    if self._current_page == 0:
      self._current_page = self._pages_cnt
    else:
      self._current_page -= 1
    return self.pages[self._current_page]

  @property
  def current_stage_text(self):
    return f'{self.current_page_number}/{self.pages_count}'
  
  @property
  def pages_count(self):
    return self._pages_cnt + 1

  @property
  def current_page_number(self):
    return self._current_page + 1

  @property
  def items_count_on_page(self):
    return self._items_count_on_page