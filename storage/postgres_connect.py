from sqlalchemy import create_engine

host = 'localhost'
host = 'db'
port = '5432'

user = 'postgres'
pwd = ''

database = 'test'
url = f'postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{database}'
print(url)

engine = create_engine(url)
conn = engine.connect()

