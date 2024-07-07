import bot
import os
#from storage import conn
#print(conn)

BOT_TOKEN = os.getenv('BOT_TOKEN')
assert BOT_TOKEN
bot.start(BOT_TOKEN)
