import redis
import pickle

redis_client = redis.Redis(host='0.0.0.0', port=6379, db=0)

def set_complex_obj(key, obj):
  redis_client.set(key, pickle.dumps(obj))

def get_complex_obj(key):
  obj = redis_client.get(key)
  return pickle.loads(obj)

