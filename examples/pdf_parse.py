import fitz
from pprint import pprint

filepath = 'pdfs/a-token_ab.pdf'

def parse_pdf(filepath):
  with fitz.open(filepath) as document:
    print(f'{document.page_count=}')
    pprint(document.metadata)
    for page in document:
      text = page.get_text()
      print(text)
parse_pdf(filepath)
