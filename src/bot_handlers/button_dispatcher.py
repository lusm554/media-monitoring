import logging

logger = logging.getLogger(__name__)

def button_dispatcher(button_handlers):
  async def _button_dispatcher(update, context):
    callback_query = update.callback_query
    await callback_query.answer()
    btn_name = callback_query.data
    logger.info(f'Clicked button {btn_name!r}')
    for btn_id, btn_callback in button_handlers.items():
      if btn_name.startswith(btn_id):
        await btn_callback(update, context)
        break
  return _button_dispatcher