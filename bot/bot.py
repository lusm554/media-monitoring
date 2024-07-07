from telegram.ext import ApplicationBuilder
from collections import namedtuple

from storage import insert_row
import scraper
from bot.setup import (
  setup_bot_data_variables,
  setup_basic_handlers,
  setup_bot_commands,
  shedule_bot_tasks,
  update_commands_ui_description,
  setup_button_dispatcher_handlers,
)
from bot.handlers import unknown_command_handler, error_handler, updates_handler
import bot.commands as bot_commands

import datetime
import logging
logging.basicConfig(
  level=logging.INFO,
  format='[%(asctime)s] %(levelname)s [%(name)s] %(message)s',
  datefmt='%Y-%m-%d %H:%M:%S %Z',
  handlers=[
    #logging.FileHandler(datetime.datetime.now().strftime('shared/logs/log_%Y-%m-%d_%H-%M-%S.log')),
    logging.StreamHandler(),
  ],
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

def setup(telegram_app):
  Command = namedtuple('Cmd', ['callback', 'desc', 'name'])
  commands = (
    Command(callback=bot_commands.start, desc='начать работу', name='start'),
    Command(callback=bot_commands.cfa_news, desc='новости ЦФА за сутки', name='last_news_cfa'),
  )
  setup_bot_data_variables(telegram_app, commands)
  setup_bot_commands(telegram_app, commands)
  setup_basic_handlers(telegram_app, error_handler, unknown_command_handler, updates_handler)
  setup_button_dispatcher_handlers(telegram_app, bot_commands.cfa_last_news_button_callback)
  #shedule_bot_tasks(telegram_app)
  update_commands_ui_description(telegram_app, commands)

def start(BOT_TOKEN):
  telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()
  setup(telegram_app)
  telegram_app.run_polling()
