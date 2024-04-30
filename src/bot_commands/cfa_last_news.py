from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from .post import Post
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

async def cfa_news_base(update, context, articles):
  if len(articles) == 0:
    await context.bot.send_message(
      chat_id=update.effective_chat.id,
      text='Новости не найдены.',
    )
    return
  post = Post(post_items=articles)
  context.bot_data['post_cache'][post.post_id] = post
  msg_text, keyboard = get_cfa_last_news_post_markup(post)
  await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text=msg_text,
    reply_markup=keyboard,
    parse_mode=ParseMode.HTML,
    disable_web_page_preview=True,
  )

async def cfa_last_news(update, context):
  scraper = context.bot_data.get("scraper")
  articles = scraper.CfaAllNewsScraper(error='ignore').fetch_and_parse(scraper.Periods.LAST_24_HOURS)
  await cfa_news_base(update, context, articles)

async def cfa_week_news(update, context):
  scraper = context.bot_data.get("scraper")
  articles = scraper.CfaAllNewsScraper(error='ignore').fetch_and_parse(scraper.Periods.LAST_WEEK)
  await cfa_news_base(update, context, articles)

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