import functools
import logging

logger = logging.getLogger(__name__)

def notify_about_chat_updates(func):
  @functools.wraps(func)
  async def wrapper(update, context):
    result = await func(update, context)
    logger.info(f'New chats list {context.bot_data.get("regular_newsletter_chats")}')
    new_version_regular_newsletter_chats = ','.join(context.bot_data.get("regular_newsletter_chats"))
    msg = f'Last version of chats `{new_version_regular_newsletter_chats!r}`'
    await context.bot.send_message(
      chat_id=context.bot_data.get('DEVELOPER_CHAT_ID'),
      text=msg
    )
    return result
  return wrapper

@notify_about_chat_updates
async def newsletter_subscribe(update, context):
  new_chat_id = str(update.effective_message.chat_id)
  time_zone = context.bot_data.get('bot_timezone')
  try:
    context.bot_data.get('regular_newsletter_chats').add(new_chat_id)
    newsletter_time = context.bot_data.get('cfa_newsletter_time')
    releases_time = context.bot_data.get('cfa_releases_time')
    msg = (
      f'Новости и выпуски ЦФА будут приходить каждый день в '
      f'{newsletter_time.strftime(f'%H:%M')} и {releases_time.strftime(f'%H:%M {time_zone}')}.\n'
      f'Чтобы отменить - /cancel_subscribe_news.'
    )
    await update.effective_message.reply_text(msg)
  except Exception as error:
    raise error

@notify_about_chat_updates
async def newsletter_cancel_subscribe(update, context):
  chat_id = str(update.effective_message.chat_id)
  try:
    context.bot_data.get('regular_newsletter_chats').remove(chat_id)
    msg = 'Подписка на новости отменена.'
    await update.effective_message.reply_text(msg)
  except KeyError:
    error_msg = (
      f'Похоже ранее Вы не подписывались на новости.\n'
      f'Воспользуйтесь /subscribe_news.'
    )
    await update.effective_message.reply_text(error_msg)