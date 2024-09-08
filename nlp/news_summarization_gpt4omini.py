from openai import OpenAI
import os

client = OpenAI(
  api_key=os.getenv('VSEGPT_API_KEY'), # ваш ключ в VseGPT после регистрации
  base_url="https://api.vsegpt.ru/v1",
)

def release_text_to_desc(prompt):
  system_text = """
  Ты анализируешь текст новостей, связанных с цифровыми финансовыми активами (ЦФА).
  Твоя задача — суммаризировать новость до 2-3 предложений, сохранив основную информацию.
  """

  messages = []
  messages.append({"role": "system", "content": system_text})
  messages.append({"role": "user", "content": prompt})

  response_big = client.chat.completions.create(
      model="openai/gpt-4o-mini", # id модели из списка моделей - можно использовать OpenAI, Anthropic и пр. меняя только этот параметр
      messages=messages,
      temperature=1,
      n=1,
      max_tokens=3000, # максимальное число ВЫХОДНЫХ токенов. Для большинства моделей не должно превышать 4096
      #extra_headers={ "X-Title": "My App" }, # опционально - передача информация об источнике API-вызова
  )
  #print("Response BIG:",response_big)
  response = response_big.choices[0].message.content
  return response

import pickle
import re
with open('t.pickle', 'rb') as f:
  t = pickle.load(f)

result = dict()
for t in t:
	text = list(t.values())[0]
	if text is None:
		result[list(t.keys())[0]] = ''
	else:
		text = re.sub(r'\s+', ' ', text)
		text = re.sub(r'[^\w\s.,!?-]', '', text)
		res = release_text_to_desc(text)
		result[list(t.keys())[0]] = res

with open('sumnews.pickle', 'wb') as f:
  pickle.dump(result, f)
with open('sumnews.pickle', 'rb') as f:
  t = pickle.load(f)
print(t)
