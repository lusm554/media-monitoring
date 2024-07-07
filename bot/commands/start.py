async def start(update, context):
  msg = (
    f'Привет!\n'
    f'Этот бот собирает публикации СМИ и выпуски по ЦФА.\n'
    f'Рассылка новостей /subscribe_news.\n'
    f'Более подробно через команду /help.'
  )
  await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text=msg
  )
