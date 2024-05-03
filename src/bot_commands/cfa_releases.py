from telegram.constants import ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from bot_helpers import Post
import logging

logger = logging.getLogger(__name__)

RIGHT_ARROW_SYMBOL = chr(8594) # →
LEFT_ARROW_SYMBOL = chr(8592) # ←
CFA_RELEASES_CALLBACK_ID = 'cfa_releases'

def get_releases_post_markup(post):
  msg_text = '\n\n'.join(
    f'{n}. <a href="{release.url}"> {release.title} </a>\n'
    f'<b>Платформа:</b> {release.platform_name}.\n'
    f'<b>Опубликовано:</b> {release.release_time}.'
    for n, release in enumerate(
      post.current_page(),
      start=(post.current_page_number - 1) * post.items_count_on_page
    )
  )
  callback_id = CFA_RELEASES_CALLBACK_ID
  internal_post_id = post.post_id
  keyboard = [
    [
      InlineKeyboardButton(LEFT_ARROW_SYMBOL, callback_data=f'{callback_id}_backward_{internal_post_id}'),
      InlineKeyboardButton(post.current_stage_text, callback_data=f'{callback_id}_counter_{internal_post_id}'),
      InlineKeyboardButton(RIGHT_ARROW_SYMBOL, callback_data=f'{callback_id}_forward_{internal_post_id}'),
    ],
  ]
  keyboard_markup = InlineKeyboardMarkup(keyboard)
  return msg_text, keyboard_markup

async def cfa_releases_base(context, effective_chat_id, releases):
  post = Post(
    post_items=sorted(releases, key=lambda x: x.platform_name),
    page_items_cnt=6,
  )
  context.bot_data['post_cache'][post.post_id] = post
  if len(releases) == 0:
    await context.bot.send_message(
      chat_id=effective_chat_id,
      text='Выпуски ЦФА не найдены.',
    )
    return
  msg_text, keyboard_markup = get_releases_post_markup(post)
  await context.bot.send_message(
    chat_id=effective_chat_id,
    text=msg_text,
    reply_markup=keyboard_markup,
    parse_mode=ParseMode.HTML,
    disable_web_page_preview=True,
  )

async def cfa_last_releases(update, context):
  scraper = context.bot_data.get("scraper")
  releases = scraper.CfaReleasesScraper(error='ignore').fetch_and_parse(scraper.Periods.LAST_24_HOURS)
  effective_chat_id = update.effective_chat.id
  await cfa_releases_base(context, effective_chat_id, releases)

async def cfa_last_releases_regular(context, effective_chat_id):
  scraper = context.bot_data.get("scraper")
  releases = scraper.CfaReleasesScraper(error='ignore').fetch_and_parse(scraper.Periods.LAST_24_HOURS)
  await cfa_releases_base(context, effective_chat_id, releases)

async def cfa_week_releases(update, context):
  scraper = context.bot_data.get("scraper")
  releases = scraper.CfaReleasesScraper(error='ignore').fetch_and_parse(scraper.Periods.LAST_WEEK)
  effective_chat_id = update.effective_chat.id
  await cfa_releases_base(context, effective_chat_id, releases)

async def cfa_all_time_releases(update, context):
  scraper = context.bot_data.get("scraper")
  releases = scraper.CfaReleasesScraper(error='ignore').fetch_and_parse(scraper.Periods.ALL_AVAILABLE_TIME)
  effective_chat_id = update.effective_chat.id
  await cfa_releases_base(context, effective_chat_id, releases)

async def cfa_releases_button_callback(update, context):
  query = update.callback_query
  btn_name = query.data
  keyboard_action, post_id = btn_name.replace(CFA_RELEASES_CALLBACK_ID + '_', '').split('_')
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
  msg_text, keyboard = get_releases_post_markup(post)
  await query.edit_message_text(
    text=msg_text,
    reply_markup=keyboard,
    parse_mode=ParseMode.HTML,
    disable_web_page_preview=True,
  )
