import logging

logger = logging.getLogger(__name__)

async def cfa_news_sender(context):
  cfa_news_callback = context.job.data
  for chat_id in context.bot_data.get('regular_newsletter_chats'):
    logger.info(f'Sending scheduled news for {chat_id}')
    await cfa_news_callback(context, chat_id)