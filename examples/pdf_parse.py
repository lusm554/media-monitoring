import fitz
from pprint import pprint

filepath = 'pdfs/a-token_ab.pdf'

def parse_pdf(filepath):
  with fitz.open(filepath) as document:
    pprint(document.metadata)

parse_pdf(filepath)
