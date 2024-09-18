from telegram.ext import ApplicationBuilder
from collections import namedtuple

from bot.setup import (
  setup_bot_data_variables,
  setup_basic_handlers,
  setup_bot_commands,
  shedule_regular_bot_tasks,
  update_commands_ui_description,
  setup_button_handlers,
)
from bot.handlers import unknown_command_handler, error_handler, updates_handler
import bot.commands as bot_commands

def setup(telegram_app):
  Command = namedtuple('Cmd', ['callback', 'desc', 'name'])
  commands = (
    Command(callback=bot_commands.start, desc='начать работу', name='start'),
    Command(callback=bot_commands.help_, desc='описание команд', name='help'),
    Command(callback=bot_commands.cfa_news, desc='новости ЦФА за сутки', name='last_news_cfa'),
    Command(callback=bot_commands.cfa_releases, desc='выпуски ЦФА за сутки', name='last_releases_cfa'),
    Command(callback=bot_commands.subscribe_news, desc='подписка на новости', name='news_subscription'),
    Command(callback=bot_commands.unsubscribe_news, desc='отмена подписки на новости', name='cancel_news_subscription'),
  )
  setup_bot_data_variables(telegram_app, commands)
  setup_bot_commands(telegram_app, commands)
  setup_basic_handlers(telegram_app, error_handler, unknown_command_handler, updates_handler)
  setup_button_handlers(telegram_app, bot_commands.cfa_last_news_button_callback, bot_commands.cfa_last_releases_button_callback)
  shedule_regular_bot_tasks(telegram_app)
  update_commands_ui_description(telegram_app, commands)

def start(BOT_TOKEN):
  telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()
  setup(telegram_app)
  telegram_app.run_polling()
