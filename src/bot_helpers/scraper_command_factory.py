from .post import Post
from telegram.constants import ParseMode

def transform_update_context(func):
  async def wrapper(update, context):
    return await func(context=context, effective_chat_id=update.effective_chat.id)
  return wrapper

def cfa_news_factory(scraper, period, get_articles, get_cfa_last_news_post_markup, *, chat_id_from_update=True):
  async def cfa_news(context, effective_chat_id):
    articles = get_articles(context, scraper, period)
    if len(articles) == 0:
      await context.bot.send_message(
        chat_id=effective_chat_id,
        text='Новости ЦФА не найдены.',
      )
      return
    post = Post(post_items=articles)
    context.bot_data['post_cache'][post.post_id] = post
    msg_text, keyboard = get_cfa_last_news_post_markup(post)
    await context.bot.send_message(
      chat_id=effective_chat_id,
      text=msg_text,
      reply_markup=keyboard,
      parse_mode=ParseMode.HTML,
      disable_web_page_preview=True,
    )
  if chat_id_from_update:
    cfa_news = transform_update_context(cfa_news)
  return cfa_news
