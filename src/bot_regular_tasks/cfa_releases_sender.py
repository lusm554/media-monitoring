import logging

logger = logging.getLogger(__name__)

async def cfa_releases_sender(context):
  cfa_releases_callback = context.job.data
  for chat_id in context.bot_data.get('regular_newsletter_chats'):
    logger.info(f'Sending scheduled releases for {chat_id}')
    await cfa_releases_callback(context, chat_id)