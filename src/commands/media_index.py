from telegram.constants import ParseMode

async def media_index(update, context):
  mindex_msg = [ 'Список отслеживаемых СМИ через RSS:' ]
  mindex = context.bot_data.get('scraper').get_rss_media_index() 
  for n, f in enumerate(mindex, start=1):
    msg = f'{n}. {f.title} ' + (f.feed_name or '').lower()
    mindex_msg.append(msg)
  mindex_msg.extend((
    f'\n<b>Список источников google не определен. Цель этого метода - максимизировать покрытие медиапространства ботом.</b>',
    f'\nДля фильтрации источников используется черный список - {context.bot_data.get("cmd").media_blacklist.cmd}.',
  ))
  mindex_msg = '\n'.join(mindex_msg)
  await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text=mindex_msg,
    parse_mode=ParseMode.HTML
  )
