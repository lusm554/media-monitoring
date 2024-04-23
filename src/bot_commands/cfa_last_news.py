import logging

logger = logging.getLogger(__name__)

async def cfa_last_news(update, context):
  scraper = context.bot_data.get("scraper")
  articles = scraper.CfaAllNewsScraper().fetch_and_parse(scraper.Periods.LAST_24_HOURS)
  help_msg = 'test'
  await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text=help_msg
  )