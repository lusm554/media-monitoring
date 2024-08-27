from bot.commands import cfa_news

async def cfa_news_sender(context):
  target_chat_id = '421489738'
  await cfa_news(context, target_chat_id)
