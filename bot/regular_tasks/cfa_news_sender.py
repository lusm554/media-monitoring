from bot.commands import cfa_news, cfa_releases
import storage

async def cfa_news_sender(context):
  # iter over news chats & send news
  #target_chat_id = '421489738'
  for subscriber in storage.get_n_news_subscribers(n=1000): # bug?
    target_chat_id = subscriber['telegram_user_id']
    await cfa_news(context, target_chat_id)

async def cfa_releases_sender(context):
  for subscriber in storage.get_n_news_subscribers(n=1000): # bug?
    target_chat_id = subscriber['telegram_user_id']
    await cfa_releases(context, target_chat_id)
