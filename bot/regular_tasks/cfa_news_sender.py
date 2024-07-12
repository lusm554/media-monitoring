async def cfa_news_sender(context):
  callback = context.job.data
  callback()
