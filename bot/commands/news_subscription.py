import storage
import datetime

async def subscribe_news(update, context):
  msg = (
    f'Новости ЦФА будут приходить в 09:00.\n'
    f'Выпуски ЦФА будут приходить в 19:00.\n'
    f'Отменить - /cancel_news_subscription.'
  )
  user = update.message.from_user
  storage.add_news_subscriber({
    'telegram_user_id': user.id,
    'add_time': datetime.datetime.now(),
  })
  print(storage.get_n_news_subscribers())
  await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text=msg
  )

async def unsubscribe_news(update, context):
  msg = 'Подписка на новости отменена.'
  user = update.message.from_user
  storage.delete_news_subscriber(user.id)
  print(storage.get_n_news_subscribers())
  await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text=msg
  )
