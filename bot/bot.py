from telegram.ext import ApplicationBuilder
from collections import namedtuple

from storage import insert_row
import scraper
from bot.setup import (
  setup_bot_data_variables,
  setup_bot_handlers,
  setup_bot_commands,
  shedule_bot_tasks,
  update_commands_ui_description,
)
#from bot.handlers import unknown_command_handler, error_handler, updates_handler
import bot.commands as bot_commands

def setup(telegram_app):
  Command = namedtuple('Cmd', ['callback', 'desc', 'name'])
  commands = (
    Command(callback=bot_commands.start, desc='начать работу', name='start'),
  )
  setup_bot_commands(telegram_app, commands)
  #setup_bot_data_variables(telegram_app, commands)
  #setup_bot_handlers(telegram_app, commands, unknown_command_handler, error_handler, updates_handler)
  #shedule_bot_tasks(telegram_app)
  update_commands_ui_description(telegram_app, commands)

def start(BOT_TOKEN):
  telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()
  setup(telegram_app)
  telegram_app.run_polling()
