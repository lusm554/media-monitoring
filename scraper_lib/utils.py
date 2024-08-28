import dateparser
import datetime

def unformatted_time2datetime(time_str):
  settings = {'TIMEZONE': 'Europe/Moscow'}
  if isinstance(time_str, datetime.datetime):
    return time_str
  try:
    parsed_dttm = dateparser.parse(time_str, settings=settings)
  except:
    parsed_dttm = datetime.datetime.now()
  return parsed_dttm

