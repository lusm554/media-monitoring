# Media Monitoring Bot

The bot is designed for operational monitoring of the media through open sources.
A telegram bot is used as a frontend.

# Arch

Backend:
  - scraper:
    - scrap news from google, dzen, most popular rss
    - scrap cfa releases
  - postgres:
    - store news, user posts, meta info
  - redis
    - cache post
  - telegram bot
    - handle user requests
    - manage post logic

Frontend:
  - Telegram bot DM




