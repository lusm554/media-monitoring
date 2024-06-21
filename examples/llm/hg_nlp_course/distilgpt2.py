from transformers import pipeline
from pprint import pprint 

generator = pipeline('text-generation', model='distilgpt2')
result = generator(
  'how are you today?',
  max_length=400,
  num_return_sequences=3,
)
pprint(result)
