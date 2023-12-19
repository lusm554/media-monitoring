import os; from env import set_env_vars; set_env_vars(filepath='.env')
import datetime
import logging
import traceback, json, html
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
  ApplicationBuilder,
  MessageHandler,
  ContextTypes,
  CommandHandler,
  TypeHandler,
  filters,
)
import scraper

logging.basicConfig(
  level=logging.INFO,
  format='[%(asctime)s] %(levelname)s [%(name)-22s] %(message)s',
  datefmt='%Y-%m-%d %H:%M:%S',
  handlers=[
    logging.FileHandler(datetime.datetime.now().strftime('logs/log_%Y-%m-%d_%H-%M-%S.log')),
    logging.StreamHandler(),
  ]
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
DEVELOPER_CHAT_ID = os.environ.get('DEVELOPER_CHAT_ID')

async def start(update, context):
  await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text='Привет! Этот бот собирает публикации СМИ по ЦФА.'
         '\nБолее подробно через команду /help.',
  )

async def unknown(update, context):
  await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text='Эта команда мне не знакома'
  )

async def help_cmd(update, context):
  help_msg = '\n'.join([
    'Описание доступных команд:',
    '/start - начало работы',
    '/help - получить инфо по командам',
    '/last_news - посмотреть новости по ключевым словам',
    '/media_index - посмотреть список отслеживаемых СМИ',
  ])
  await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text=help_msg
  )

def is_cache_expire(context):
  if (datetime.datetime.now() - context.bot_data['news_cache']['timestamp']).seconds // 60 > 10:
    logger.info(f"Cache date {context.bot_data['news_cache']['timestamp']} expire")
    return True
  return False

async def cfa_info(update, context):
  if context.bot_data['news_cache'] is None or is_cache_expire(context):
    cfa_markup = [
      'За последнее время были опубликованы следующие новости:',
    ]
    news = context.bot_data.get('scraper').get_articles()
    for n, article in enumerate(news, start=1):
      publisher = article.publisher_name
      title = article.title
      url = article.url
      publish_time = article.publish_time.strftime('%Y-%m-%d %H:%M:%S')
      scraper_type = article.scraper
      article_markup = (
        f'{n}. <a href="{url}"> {title} </a>\n'
        f'<b>Источник:</b> {publisher}.\n'
        f'<b>Опубликовано:</b> {publish_time}.\n'
        f'<b>Взято из:</b> {scraper_type}.'
      )
      cfa_markup.append(article_markup)
    logger.info(f'Updating cache')
    context.bot_data['news_cache'] = {
      'markup': cfa_markup,
      'timestamp': datetime.datetime.now(),
    }
  else:
    logger.info(f"Return message from cache on {context.bot_data['news_cache']['timestamp']}")
    cfa_markup = context.bot_data.get('news_cache')['markup']

  batched_markup = [cfa_markup[i:i + 15] for i in range(0, len(cfa_markup), 15)]
  for msg_markup in batched_markup:
    _makrup = '\n\n'.join(msg_markup)
    await context.bot.send_message(
      chat_id=update.effective_chat.id,
      text=_makrup,
      parse_mode=ParseMode.HTML
    )

async def media_index(update, context):
  mindex_msg = [
    'Список отслеживаемых СМИ через RSS:',
  ]
  mindex = context.bot_data.get('scraper').get_rss_media_index() 
  for n, f in enumerate(mindex, start=1):
    msg = f'{n}. {f.title} ' + (f.feed_name or '').lower()
    mindex_msg.append(msg)
  mindex_msg = '\n'.join(mindex_msg)
  await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text=mindex_msg
  )

async def error_handler(update, context):
  logger.error("Exception while handling an update:", exc_info=context.error)
  tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
  tb_string = "".join(tb_list)
  update_str = update.to_dict() if isinstance(update, Update) else str(update)
  message = (
    "An exception was raised while handling an update\n"
    f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
    "</pre>\n\n"
    f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
    f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
    f"<pre>{html.escape(tb_string)}</pre>"
  )
  await context.bot.send_message(
    chat_id=DEVELOPER_CHAT_ID, text=message, parse_mode=ParseMode.HTML
  )

async def callback(update, context):
  try:
    show_obj = {
      'user': update.message.from_user,
      'chat': update.message.chat,
      'text': update.message.text,
    }
    logger.info(f'Update: {show_obj!r}')
  except:
    logger.info(f'Update: {update!r}')

def main():
  TOKEN = os.environ.get('TELEGRAM_TOKEN')
  app = ApplicationBuilder().token(TOKEN).build() 

  # Add news scraper
  app.bot_data['scraper'] = scraper.get_scraper_instance(
    rss_scrp=scraper.RSS,
    go_scrp=scraper.GoogleScraper,
    article_wrp=scraper.WrappedArticle
  )
  # Add cache
  app.bot_data['news_cache'] = None

  # Logger
  app.add_handler(TypeHandler(Update, callback), -1)

  # Register commands 
  app.add_handler(CommandHandler('start', start))
  app.add_handler(CommandHandler('help', help_cmd))
  app.add_handler(CommandHandler('last_news', cfa_info))
  app.add_handler(CommandHandler('media_index', media_index))

  # Unknown cmd handler
  unknown_handler = MessageHandler(filters.COMMAND, unknown)
  app.add_handler(unknown_handler)

  # Error handler
  app.add_error_handler(error_handler)

  # Run until Ctrl-C
  app.run_polling()

if __name__ == '__main__':
  main()
