import os
import logging
__all__ = ['set_env_vars']

logger = logging.getLogger(__name__)

def set_env_vars(filepath):
  try:
    with open(filepath, 'r') as file:
      for line in file:
        if not '=' in line: continue
        key, value = tuple(map(str.strip, line.split('=')))
        logger.info(f'{key} {value}')
        os.environ[key] = value
  except Exception as error:
    logger.info('Cannot parse .env file. Env vars will be read from environ.')
