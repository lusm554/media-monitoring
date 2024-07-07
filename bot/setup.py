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
  '''
  telegram_app.bot_data['commands'] = commands
  telegram_app.bot_data['scraper'] = scraper
  telegram_app.bot_data['post_cache'] = dict()
  telegram_app.bot_data['scraper_cache'] = dict()
  #telegram_app.bot_data['regular_newsletter_chats'] = set(str(x) for x in os.environ.get('NEWS_SCHEDULED_CHATS').split(',') if x != '')
  telegram_app.bot_data['bot_timezone'] = time_zone_moscow
  telegram_app.bot_data['cfa_newsletter_time'] = datetime.time(hour=9, tzinfo=time_zone_moscow)
  telegram_app.bot_data['cfa_releases_time'] = datetime.time(hour=19, tzinfo=time_zone_moscow)
  telegram_app.bot_data['DEVELOPER_CHAT_ID'] = os.environ.get('DEVELOPER_CHAT_ID')
  telegram_app.bot_data['commands'] = commands
  '''

def setup_bot_commands(telegram_app, commands):
  for command in commands:
    telegram_app.add_handler(
      CommandHandler(
        command=command.name,
        callback=command.callback
      )
    )

def setup_bot_handlers(telegram_app, commands, unknown_command_handler, error_handler, updates_handler):
  telegram_app.add_handler(TypeHandler(Update, updates_handler), -1)
  for command in commands:
    telegram_app.add_handler(
      CommandHandler(
        command=command.name,
        callback=command.callback
      )
    )
  '''
  telegram_app.add_handler(
    CallbackQueryHandler(
      bot_handlers.button_dispatcher({
        'cfa_last_news': bot_commands.cfa_last_news_button_callback,
        'cfa_releases': bot_commands.cfa_releases_button_callback,
      })
    )
  )
  '''
  telegram_app.add_handler(MessageHandler(filters.COMMAND, unknown_command_handler))
  telegram_app.add_error_handler(error_handler)

def shedule_bot_tasks(telegram_app):
  job_interval = datetime.timedelta(hours=1)
  job_time_to_first_run = datetime.timedelta(seconds=30)
  newsletter_time = telegram_app.bot_data.get('cfa_newsletter_time')
  releases_time = telegram_app.bot_data.get('cfa_releases_time')
  telegram_app.job_queue.run_repeating(
    callback=bot_regular_tasks.post_cache_cleaner,
    interval=job_interval,
    first=job_time_to_first_run,
  )
  telegram_app.job_queue.run_daily(
    callback=bot_regular_tasks.cfa_news_sender,
    time=newsletter_time,
    data=bot_commands.cfa_last_news_regular,
  )
  telegram_app.job_queue.run_daily(
    callback=bot_regular_tasks.cfa_releases_sender,
    time=releases_time,
    data=bot_commands.cfa_last_releases_regular,
  )
  # telegram_app.job_queue.run_repeating(
  #   bot_regular_tasks.cfa_news_sender,
  #   interval=60,
  #   first=15,
  #   data=bot_commands.cfa_last_releases_regular,
  # )

def update_commands_ui_description(telegram_app, commands):
  cmds = [
    BotCommand(command=cmd.name, description=cmd.desc)
    for cmd in commands
  ]
  loop = asyncio.get_event_loop()
  loop.run_until_complete(telegram_app.bot.set_my_commands(cmds))
