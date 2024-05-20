import fitz
import re
import os
from pprint import pprint

def pdf_to_text(filepath):
  with fitz.open(filepath) as document:
    document_text = ''
    for page in document:
      text = page.get_text()
      document_text += text
  #document_text = document_text.replace('\n', ' ')
  #document_text = re.sub(" +", " ", document_text)
  #document_text = document_text.strip()
  return document_text


def main():
  filepath = 'pdfs/a-token_alrosa.pdf'
  filetext = pdf_to_text(filepath)
  print(filetext)
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
