from telegram import Update, BotCommand
from telegram.constants import ParseMode
from telegram.ext import (
  ApplicationBuilder,
  MessageHandler,
  ContextTypes,
  CommandHandler,
  TypeHandler,
  CallbackQueryHandler,
  filters,
)
import asyncio

def setup_bot_data_variables(telegram_app, commands):
	pass

def setup_bot_commands(telegram_app, commands):
  for command in commands:
    telegram_app.add_handler(
      CommandHandler(
        command=command.name,
        callback=command.callback
      )
    )

def setup_basic_handlers(telegram_app, error_handler, unknown_command_handler, updates_handler):
  telegram_app.add_handler(TypeHandler(Update, updates_handler), -1)
  telegram_app.add_handler(MessageHandler(filters.COMMAND, unknown_command_handler))
  telegram_app.add_error_handler(error_handler)

def update_commands_ui_description(telegram_app, commands):
  cmds = [
    BotCommand(command=cmd.name, description=cmd.desc)
    for cmd in commands
  ]
  loop = asyncio.get_event_loop()
  loop.run_until_complete(telegram_app.bot.set_my_commands(cmds))

def setup_button_dispatcher_handlers():
	pass

def shedule_bot_tasks(telegram_app):
	pass
