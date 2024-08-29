import storage
import datetime

async def start(update, context):
  msg = (
    f'Привет!\n'
    f'Этот бот собирает публикации СМИ и выпуски по ЦФА.\n'
    f'Рассылка новостей /subscribe_news.\n'
    f'Более подробно через команду /help.'
  )
  user = update.message.from_user
  user_start_time = datetime.datetime.now()
  storage.add_user({
    'telegram_user_id': user.id,
    'add_time': user_start_time,
    'update_time': user_start_time,
    'telegram_username': user.username,
    'telegram_first_name': user.first_name,
  })
  await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text=msg
  )
