from storage.postgres_client import (
  connect, create_tables_if_not_exists, recreate_tables,
  add_news, get_n_news, get_last_24h_news,
  #get_news_by_date_range,
  get_n_users, add_user,
  add_news_subscriber, get_n_news_subscribers, delete_news_subscriber,
  get_n_news_posts, get_news_post, get_articles_by_news_post, add_news_posts,
  add_releases, add_releases_posts, get_n_releases_posts, get_n_releases, get_last_24h_releases, 
  get_releases_by_release_post,
  get_releases, get_news
)
from storage import redis_client
