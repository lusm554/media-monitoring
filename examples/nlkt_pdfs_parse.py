from pprint import pprint
import fitz
import re, os

import nltk
nltk.download('punkt')

def pdf_to_text(filepath):
  with fitz.open(filepath) as document:
    document_text = ''
    for page in document:
      text = page.get_text()
      document_text += text
  return document_text

def preprocess_text(text):
  text = text.lower()
  text = re.sub(r'\s+', ' ', text)
  text = re.sub(r'[^\w\s]', '', text)
  return text

def tokenize_text(text):
  tokens = nltk.word_tokenize(text, language='russian')
  return tokens

def lemmatize_tokens(tokens):
  from pymystem3 import Mystem
  mystem = Mystem()
  lemmatized_tokens = mystem.lemmatize(' '.join(tokens))
  lemmatized_tokens = [token for token in lemmatized_tokens if token.strip()]
  return lemmatized_tokens

def extract_values(tokens, keywords):
  values = list()
  for i, token in enumerate(tokens):
    if token in keywords:
      context_window = tokens[max(0, i-5):i+5]
      values.append((token, context_window))
  return values

def parse_context(context_window, keyword):
  for word in context_window:
    if keyword == 'приобретение' and word.isdigit():
      return f"Номинал: {word}"
  return None

def main():
  filepath = 'pdfs/a-token_alrosa.pdf'
  filetext = pdf_to_text(filepath)
  filetext = preprocess_text(filetext)
  tokens = tokenize_text(filetext)
  lemmatized_tokens = lemmatize_tokens(tokens)
  keywords = ['приобретение']
  extracted_values = extract_values(lemmatized_tokens, keywords)
  for kw, context in extracted_values:
    result = parse_context(context, kw)
    if result:
      print(result)
  '''
  for root, dirs, files in os.walk('pdfs/'):
    for file in files:
      filepath = os.path.join(root, file)
      if file.startswith('a-token'): 
        print(filepath)
        parse_pdf(filepath, atoken_patterns)
      if file.startswith('sberbank'):
        continue
        print(filepath)
        parse_pdf(filepath, sberbank_patterns)
        pass
      if file.startswith('tokeon'):
        continue
        print(filepath)
        parse_pdf(filepath, tokeon_patterns)
        pass
  '''

if __name__ == '__main__':
  main()
