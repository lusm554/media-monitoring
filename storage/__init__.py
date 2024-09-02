from storage.postgres_client import (
  connect, create_tables_if_not_exists, recreate_tables, add_news, get_news_by_date_range, get_n_news,
  get_last_24h_news, get_n_users,
	add_news_subscriber, get_n_news_subscribers, delete_news_subscriber,
  #add_news_post,
  get_n_news_posts, get_news_post, get_articles_by_news_post,
  #select_n_news
  add_users, add_news, add_news_posts, add_news_subscriber, add_releases, add_releases_posts,
  get_n_releases_posts, get_n_releases
)
from storage import redis_client
