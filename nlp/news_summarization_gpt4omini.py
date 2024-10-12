from openai import OpenAI
import os

client = OpenAI(
  api_key=os.getenv('VSEGPT_API_KEY'), # ваш ключ в VseGPT после регистрации
  base_url="https://api.vsegpt.ru/v1",
)

def news_text_summarization(news_test):
  system_text = """
  Ты анализируешь текст новостей, связанных с цифровыми финансовыми активами (ЦФА).
  Твоя задача — суммаризировать новость до 2-3 предложений, сохранив основную информацию.
  """

  messages = []
  messages.append({"role": "system", "content": system_text})
  messages.append({"role": "user", "content": news_test})

  response_big = client.chat.completions.create(
    model="openai/gpt-4o-mini", # id модели из списка моделей - можно использовать OpenAI, Anthropic и пр. меняя только этот параметр
    messages=messages,
    temperature=0,
    n=1,
    max_tokens=3000, # максимальное число ВЫХОДНЫХ токенов. Для большинства моделей не должно превышать 4096
    #extra_headers={ "X-Title": "My App" }, # опционально - передача информация об источнике API-вызова
  )
  #print("Response BIG:",response_big)
  response = response_big.choices[0].message.content
  return response

