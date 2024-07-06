from sentence_transformers import SentenceTransformer
model = SentenceTransformer('cointegrated/rubert-tiny2')
sentences = ["привет мир", "hello world", "здравствуй вселенная"]
embeddings = model.encode(sentences)
print(embeddings)
