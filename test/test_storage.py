import sys; sys.path.insert(0, '.')
import storage
from storage import postgres_datamap 

storage.recreate_tables()
#storage.create_tables_if_not_exists()

#################### Add rows ####################
import datetime

def test_add_postgres(row, rows, testing_add, testing_get_n_rows):
  # one row insert
  testing_add(row)
  assert len(testing_get_n_rows()) == 1, testing_get_n_rows()

  # multiple rows with same id col
  equal_rows = [row for i in range(5)]
  testing_add(equal_rows)
  assert len(testing_get_n_rows()) == 1, testing_get_n_rows()

  # multiple unique rows
  testing_add(rows)
  assert len(testing_get_n_rows()) == len(rows)+1, testing_get_n_rows()

# Test add_users
test_add_postgres(
  row={
    'telegram_user_id': 24,
    'add_time': datetime.datetime.now(),
    'update_time': datetime.datetime.now(),
    'telegram_username': 'abobus',
    'telegram_first_name': 'abobus',
  },
  rows=[
    {
      'telegram_user_id': i,
      'add_time': datetime.datetime.now(),
      'update_time': datetime.datetime.now(),
      'telegram_username': 'abobus',
      'telegram_first_name': 'abobus',
    }
    for i in range(5)
  ],
  testing_add=storage.add_users,
  testing_get_n_rows=storage.get_n_users,
)

# Test add_news
test_add_postgres(
  row={
    "title": "test",
    "url": "https",
    "publish_time": datetime.datetime.now(),
    "publisher_name": "test",
    "body_text": "test",
    "scraper": "test",
    "db_id": 123,
  },
  rows=[
    {
      "title": "test",
      "url": f"https{i}",
      "publish_time": datetime.datetime.now(),
      "publisher_name": "test",
      "body_text": "test",
      "scraper": "test",
      "db_id": 123,
    }
    for i in range(5)
  ],
  testing_add=storage.add_news,
  testing_get_n_rows=storage.get_n_news,
)

# Test add_news_posts
test_add_postgres(
  row={ 'bot_post_id': 'adsf', 'news_id': 1, },
  rows=[{ 'bot_post_id': f'adsf{i}', 'news_id': 1, } for i in range(5)],
  testing_add=storage.add_news_posts,
  testing_get_n_rows=storage.get_n_news_posts,
)

# Test add_releases_posts
test_add_postgres(
  row={ 'bot_post_id': 'adsf', 'release_id': 1, },
  rows=[{ 'bot_post_id': f'adsf{i}', 'release_id': 1, } for i in range(5)],
  testing_add=storage.add_releases_posts,
  testing_get_n_rows=storage.get_n_releases_posts,
)

test_add_postgres(
  row={
    'platform_name': 'test',
    'url': 'test',
    'release_time': datetime.datetime.now(),
    'title': 'test',
  },
  rows=[
    {
      'platform_name': 'test',
      'url': f'test{i}',
      'release_time': datetime.datetime.now(),
      'title': 'test',
    }
    for i in range(5)
  ],
  testing_add=storage.add_releases,
  testing_get_n_rows=storage.get_n_releases,
)
