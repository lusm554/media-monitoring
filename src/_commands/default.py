async def start(update, context):
  await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text=f'Привет! Этот бот собирает публикации СМИ по ЦФА.\n'
         f'Более подробно через команду {context.bot_data.get("cmd").help.cmd}.',
  )

async def unknown(update, context):
  await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text='Эта команда мне не знакома.'
  )

async def help_cmd(update, context):
  help_msg = '\n'.join(
    f'{c.cmd} - {c.desc}'
    for c in sorted(
      [getattr(context.bot_data.get("cmd"), field) for field in context.bot_data.get("cmd")._fields],
      key=lambda x: x.ord
    )
  )
  await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text=help_msg
  )
