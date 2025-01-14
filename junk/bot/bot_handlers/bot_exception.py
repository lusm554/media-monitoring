import traceback, json, html
from telegram import Update
from telegram.constants import ParseMode
import logging

logger = logging.getLogger(__name__)

async def error_handler(update, context):
  logger.error("Exception while handling an update:", exc_info=context.error)
  tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
  tb_string = "".join(tb_list)
  update_str = update.to_dict() if isinstance(update, Update) else str(update)
  update_html = html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))
  update_html = update_html[:2000]
  message = (
    f"An exception was raised while handling an update\n"
    f"<pre>update = {update_html}"
    f"</pre>\n\n"
    f"<pre>{html.escape(tb_string)}</pre>"
  )
  logger.info(f'Error message size {len(message)}')
  await context.bot.send_message(
    chat_id=context.bot_data.get('DEVELOPER_CHAT_ID'),
    text=message,
    parse_mode=ParseMode.HTML,
  )