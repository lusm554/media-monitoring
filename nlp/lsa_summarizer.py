from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer

def get_russian_stopwords():
  with open('nlp/russian_stop_words.txt', 'rt') as f:
    data = f.read()
  return frozenset(w.rstrip() for w in data.splitlines() if w)

def lsa_summarizer(text):
  LANGUAGE = "russian"
  SENTENCES_COUNT = 3
  parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
  summarizer = Summarizer(Stemmer(LANGUAGE))
  summarizer.stop_words = get_russian_stopwords()
  summirized = '\n'.join(str(sen) for sen in summarizer(parser.document, SENTENCES_COUNT))
  return summirized
