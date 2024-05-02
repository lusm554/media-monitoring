from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from .post import Post
import scraper
import logging

logger = logging.getLogger(__name__)

RIGHT_ARROW_SYMBOL = chr(8594) # →
LEFT_ARROW_SYMBOL = chr(8592) # ←
CFA_LAST_NEWS_CALLBACK_ID = 'cfa_last_news'

def get_cfa_last_news_post_markup(post):
  msg = '\n\n'.join(
    f'{n}. <a href="{article.url}"> {article.title} </a>\n'
    f'<b>Источник:</b> {article.publisher_name}.\n'
    f'<b>Опубликовано:</b> {article.publish_time}.\n'
    f'<b>Взято из:</b> {article.scraper}.'
    for n, article in enumerate(
      post.current_page(),
      start=(post.current_page_number - 1) * post.items_count_on_page
    )
  )
  internal_post_id = post.post_id
  callback_id = CFA_LAST_NEWS_CALLBACK_ID
  pagination_keyboard = [
    [
      InlineKeyboardButton(LEFT_ARROW_SYMBOL, callback_data=f'{callback_id}_backward_{internal_post_id}'),
      InlineKeyboardButton(post.current_stage_text, callback_data=f'{callback_id}_counter_{internal_post_id}'),
      InlineKeyboardButton(RIGHT_ARROW_SYMBOL, callback_data=f'{callback_id}_forward_{internal_post_id}')
    ],
  ]
  keyboard_markup = InlineKeyboardMarkup(pagination_keyboard)
  return msg, keyboard_markup

def transform_update_context(func):
  async def wrapper(update, context):
    return await func(context=context, effective_chat_id=update.effective_chat.id)
  return wrapper

def cfa_news_factory(scraper, period, *, chat_id_from_update=True):
  async def cfa_news(context, effective_chat_id):
    articles = scraper.CfaAllNewsScraper(error='ignore').fetch_and_parse(period)
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

cfa_last_news = cfa_news_factory(
  scraper=scraper,
  period=scraper.Periods.LAST_24_HOURS,
)

cfa_last_news_regular = cfa_news_factory(
  scraper=scraper,
  period=scraper.Periods.LAST_24_HOURS,
  chat_id_from_update=False,
)

cfa_week_news = cfa_news_factory(
  scraper=scraper,
  period=scraper.Periods.LAST_WEEK,
)

async def cfa_last_news_button_callback(update, context):
  query = update.callback_query
  btn_name = query.data
  keyboard_action, post_id = btn_name.replace(CFA_LAST_NEWS_CALLBACK_ID + '_', '').split('_')
  post = context.bot_data['post_cache'].get(post_id)
  if post is None:
    await context.bot.send_message(
      chat_id=query.message.chat.id,
      reply_to_message_id=query.message.message_id,
      text='По некоторым причинам кеш этого поста не найден, поэтому действие недоступно.'
    )
    return
  if post.pages_count == 1:
    return
  match keyboard_action:
    case 'counter':
      return
    case 'forward':
      post.next_page()
    case 'backward':
      post.previous_page()
  msg_text, keyboard = get_cfa_last_news_post_markup(post)
  await query.edit_message_text(
    text=msg_text,
    reply_markup=keyboard,
    parse_mode=ParseMode.HTML,
    disable_web_page_preview=True,
  )