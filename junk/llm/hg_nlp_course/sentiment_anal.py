from transformers import pipeline
from pprint import pprint

classifier = pipeline('sentiment-analysis')
result = classifier('hello!') 
pprint(result)

several_sentences = [
  'wtf are you doing',
  'Oh, hello! How are you today?',
  'ты на кого батон крошишь?',
  'very nice day, very sunny',
]
result = classifier(several_sentences) 
pprint(dict(zip(several_sentences, result)))
