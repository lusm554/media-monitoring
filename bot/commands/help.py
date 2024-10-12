async def help_(update, context):
  commands_desc = '\n'.join(f"/{c.name} - {c.desc}" for c in context.bot_data['bot_commands'])
  msg = (
    f'Команды бота:\n'
    f'{commands_desc}'
  )
  await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text=msg
  )
