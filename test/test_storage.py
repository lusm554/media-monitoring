import sys; sys.path.insert(0, '.')
import storage
from storage import postgres_datamap 

storage.recreate_tables()
#storage.create_tables_if_not_exists()

#################### Add rows ####################
import datetime

def test_add_users():
  user_row = {
    'telegram_user_id': 1,
    'add_time': datetime.datetime.now(),
    'update_time': datetime.datetime.now(),
    'telegram_username': 'abobus',
    'telegram_first_name': 'abobus',
  }
  storage.add_users(user_row)
  assert len(storage.get_n_users()) == 1, storage.get_n_users()

  user_rows = [user_row for i in range(5)]
  storage.add_users(user_rows)
  assert len(storage.get_n_users()) == 1, storage.get_n_users()

  user_rows = [
    {
      'telegram_user_id': i,
      'add_time': datetime.datetime.now(),
      'update_time': datetime.datetime.now(),
      'telegram_username': 'abobus',
      'telegram_first_name': 'abobus',
    }
    for i in range(5)
  ]
  storage.add_users(user_rows)
  assert len(storage.get_n_users()) == 5, storage.get_n_users()

def test_add_news():
  # add news test
  news_row = {
    "title": "test",
    "url": "https",
    "publish_time": datetime.datetime.now(),
    "publisher_name": "test",
    "body_text": "test",
    "scraper": "test",
  }
  storage.add_news(news_row)
  assert len(storage.get_n_news()) == 1, storage.get_n_news()

  # filter duplicates test
  news_rows = [news_row for i in range(5)]
  storage.add_news(news_rows)
  assert len(storage.get_n_news()) == 1, storage.get_n_news()
  
  # multiple add test
  news_rows = [
    {
        "title": "test",
        "url": f"https{i}",
        "publish_time": datetime.datetime.now(),
        "publisher_name": "test",
        "body_text": "test",
        "scraper": "test",
    }
    for i in range(5)
  ]
  storage.add_news(news_rows)
  assert len(storage.get_n_news()) == 6, storage.get_n_news()

def test_add_news_posts():
  # add news test
  news_posts_row = {
    'bot_post_id': 'adsf',
    'news_id': 1,
  }
  storage.add_news_posts(news_posts_row)
  assert len(storage.get_n_news_posts()) == 1, storage.get_n_news_posts()

  # filter duplicates test
  news_posts_rows = [news_posts_row for i in range(5)]
  storage.add_news_posts(news_posts_rows)
  assert len(storage.get_n_news_posts()) == 1, storage.get_n_news_posts()
  
  # multiple add test
  news_posts_rows = [
    {
      'bot_post_id': f'adsf{i}',
      'news_id': 1,
    }
    for i in range(5)
  ]
  storage.add_news_posts(news_posts_rows)
  assert len(storage.get_n_news_posts()) == 6, storage.get_n_news_posts()

test_add_news_posts()
test_add_news()
test_add_users()

