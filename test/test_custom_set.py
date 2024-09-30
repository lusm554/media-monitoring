import sys; sys.path.insert(0, '.')
from scraper_lib import Article
import datetime 

arts = [
  Article.from_dict({'title': 'test', 'url': 'https://www.kp40.ru/site/releases/company/116925/', 'publish_time': datetime.datetime.now(), 'publisher_name': 'test', 'scraper': 'dzen'}),
  Article.from_dict({'title': 'test', 'url': 'https://www.kp40.ru/site/releases/company/116925?a=1', 'publish_time': datetime.datetime.now(), 'publisher_name': 'test', 'scraper': 'dzen'})
]

print(len(arts))
print(len(set(arts)))
arts = list(set(arts))
for a in arts: a.set_hash_attr('title')
print(arts)
print(len(set(arts)))

