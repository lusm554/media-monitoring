from telegram.constants import ParseMode

async def media_blacklist(update, context):
  msg = [ 'Список СМИ, которые входят в blacklist:' ]
  blacklist = context.bot_data.get('scraper').get_media_blacklist() 
  for n, i in enumerate(blacklist, start=1):
    _msg = f'{n}. {i} '
    msg.append(_msg)
  msg.append(
    '\n<b>Список распространяется на все способы получения новостей (rss, google).</b>',
  )
  markup = '\n'.join(msg)
  await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text=markup,
    parse_mode=ParseMode.HTML
  )
