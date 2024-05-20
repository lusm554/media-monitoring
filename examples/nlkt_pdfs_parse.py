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
  tokens = nltk.word_tokenize(text)
  return tokens

def main():
  filepath = 'pdfs/a-token_alrosa.pdf'
  filetext = pdf_to_text(filepath)
  filetext = preprocess_text(filetext)
  tokens = tokenize_text(filetext)
  print(tokens)
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
