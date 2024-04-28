import logging

logger = logging.getLogger(__name__)

class Post:
  def __init__(self, post_id, post_articles, creation_time=None):
    self._post_count_on_page = 4
    self._current_page = 0
    self.post_id = str(post_id)
    self.post_articles = post_articles
    self.pages = [
      self.post_articles[i:i+self._post_count_on_page]
      for i in range(0, len(self.post_articles), self._post_count_on_page)
    ]
    self._pages_size = len(self.pages) - 1
    self.creation_time = creation_time or datetime.datetime.now()

  def current_page(self):
    return self.pages[self._current_page]

  def next_page(self):
    if self._current_page == self._pages_size:
      self._current_page = 0
    else:
      self._current_page += 1
    return self.pages[self._current_page]

  def previous_page(self):
    if self._current_page == 0:
      self._current_page = self._pages_size
    else:
      self._current_page -= 1
    return self.pages[self._current_page]

  @property
  def current_stage_text(self):
    return f'{self._current_page+1}/{self._pages_size+1}'
async def cfa_last_news(update, context):
  scraper = context.bot_data.get("scraper")
  articles = scraper.CfaAllNewsScraper().fetch_and_parse(scraper.Periods.LAST_24_HOURS)
  help_msg = 'test'
  await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text=help_msg
  )