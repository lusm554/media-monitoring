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
import datetime
from bot.regular_tasks import cfa_news_sender
import asyncio

def setup_bot_data_variables(telegram_app, commands):
  telegram_app.bot_data['post_cache'] = dict()

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

def setup_button_handlers(telegram_app, cfa_last_news_button_callback):
  telegram_app.add_handler(CallbackQueryHandler(cfa_last_news_button_callback, pattern='cfa_last_news*')) 

def shedule_bot_tasks(telegram_app):
  job_interval = datetime.timedelta(seconds=30)
  telegram_app.job_queue.run_repeating(
    callback=cfa_news_sender,
    interval=job_interval,
    data=lambda: print('hello'),
    first=datetime.timedelta(seconds=30),
  )
