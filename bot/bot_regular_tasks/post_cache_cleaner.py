import datetime
import logging

logger = logging.getLogger(__name__)

async def post_cache_cleaner(context):
  post_cache_expiration_delta = datetime.timedelta(hours=36)
  _cnt_of_expired_posts = 0
  for post_id, post in list(context.bot_data.get('post_cache', dict()).items()):
    post_creation_time_threshold = datetime.datetime.now() - post_cache_expiration_delta
    if post.creation_time < post_creation_time_threshold:
      logger.info(f'Post cache {post_id} expired')
      del context.bot_data['post_cache'][post_id]
      _cnt_of_expired_posts += 1
  logger.info(f'Found {_cnt_of_expired_posts} expired posts')