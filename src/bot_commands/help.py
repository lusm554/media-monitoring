async def help_(update, context):
  help_msg = '\n'.join(
    f'/{cmd.name} - {cmd.desc}'
    for cmd in context.bot_data.get("commands", [])
  )
  await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text=help_msg
  )