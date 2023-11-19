import os
__all__ = ['set_env_vars']

def set_env_vars(filepath):
  try:
    with open(filepath, 'r') as file:
      for line in file:
        if not '=' in line: continue
        key, value = tuple(map(str.strip, line.split('=')))
        os.environ[key] = value
  except Exception as error:
    print('Cannot parse .env file.')
    raise error
