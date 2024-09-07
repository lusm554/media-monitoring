def pdf_to_text(pdf_filepath):
	from pdfminer.high_level import extract_text
	import re
	text = extract_text("cfa.pdf")
	text = re.sub(r'\s+', ' ', text) 
	text = re.sub(r'[^\w\s.,!?-]', '', text)
	print(len(text))
	return text
