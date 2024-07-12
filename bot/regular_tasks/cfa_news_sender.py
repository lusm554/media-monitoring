from bot.commands import cfa_news

async def cfa_news_sender(context):
  target_chat_id = ''
  await cfa_news(context, target_chat_id)
