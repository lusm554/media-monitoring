import os; from env import set_env_vars; set_env_vars(filepath='.env')
import logging
import traceback, json, html
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
  ApplicationBuilder,
  MessageHandler,
  ContextTypes,
  CommandHandler,
  filters
)
from rss_parser import last_news_rss, RSS_FEEDS


logging.basicConfig(
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
  level=logging.INFO,
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
    text='Эта команда мне не знакома :/'
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

async def cfa_info(update, context):
  news = last_news_rss()
  cfa_msg = [
    'За последнее время были опубликованы следующие новости:',
  ]
  for n, (arc_src, article) in enumerate(news, start=1):
    src_title = arc_src.title
    title = article.title
    link = article.link
    pub_time = article.published
    msg = f'{n}. <a href="{link}"> {title} </a>\n<b>Источник:</b> {src_title}.\n<b>Опубликовано:</b> {pub_time}.'
    cfa_msg.append(msg)
  
  cfa_msg = '\n\n'.join(cfa_msg)
  await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text=cfa_msg,
    parse_mode=ParseMode.HTML
  )

async def media_index(update, context):
  mindex_msg = [
    'Список отслеживаемых СМИ:',
  ]
  for n, f in enumerate(RSS_FEEDS, start=1):
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


def main():
  TOKEN = os.environ.get('TELEGRAM_TOKEN')
  app = ApplicationBuilder().token(TOKEN).build() 

  # Register commands 
  app.add_handler(CommandHandler('start', start))
  app.add_handler(CommandHandler('help', help_cmd))
  app.add_handler(CommandHandler('last_news', cfa_info))
  app.add_handler(CommandHandler('media_index', media_index))

  unknown_handler = MessageHandler(filters.COMMAND, unknown)
  app.add_handler(unknown_handler)

  # Error handler
  app.add_error_handler(error_handler)

  # Run until Ctrl-C
  app.run_polling()

if __name__ == '__main__':
  main()
