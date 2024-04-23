import logging

logger = logging.getLogger(__name__)

async def updates_logger(update, context):
  try:
    show_obj = {
      'user': update.message.from_user,
      'chat': update.message.chat,
      'text': update.message.text,
    }
    logger.info(f'Update: {show_obj!r}')
  except:
    logger.info(f'Update id: {update.update_id!r}')