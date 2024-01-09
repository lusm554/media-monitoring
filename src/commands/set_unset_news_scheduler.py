import logging
import functools

logger = logging.getLogger(__name__)

def notify_about_chat_updates(func):
  @functools.wraps(func)
  async def wrapper(update, context):
    result = await func(update, context)
    logger.info('Sending last version of chats to dev chat')
    _chats = ','.join(context.bot_data.get("news_scheduled_chats"))
    message = f'Last version of chats {_chats!r}'
    await context.bot.send_message(
      chat_id=context.bot_data.get('DEVELOPER_CHAT_ID'),
      text=message
    )
    return result
  return wrapper

@notify_about_chat_updates
async def set_sheduler_cfa_info(update, context):
  chat_id = str(update.effective_message.chat_id)
  time_zone = context.bot_data.get('timezone')
  try:
    context.bot_data.get('news_scheduled_chats').add(chat_id)
    logger.info(f'News scheduler chats after added new chat {context.bot_data.get("news_scheduled_chats")}')
    schedule_time_str = context.bot_data.get('news_scheduled_time').strftime(f'%H:%M {time_zone}')
    msg = (
      f'Новости будут приходить в {schedule_time_str} каждый день.\n'
      f'Чтобы отменить - {context.bot_data.get("cmd").unset_news_schedule.cmd}.'
    )
    await update.effective_message.reply_text(msg)
  except Exception as error:
    raise error

@notify_about_chat_updates
async def unset_sheduler_cfa_info(update, context):
  chat_id = str(update.effective_message.chat_id)
  try:
    context.bot_data.get('news_scheduled_chats').remove(chat_id)
    logger.info(f'News scheduler chats after removed chat {context.bot_data.get("news_scheduled_chats")}')
    msg = 'Запланированные новости выключены.'
    await update.effective_message.reply_text(msg)
  except KeyError:
    error_msg = (
      f'Похоже ранее новости не планировались.\n'
      f'Воспользуйтесь {context.bot_data.get("cmd").set_news_schedule.cmd}.'
    )
    await update.effective_message.reply_text(error_msg)
