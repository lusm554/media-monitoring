from openai import OpenAI
import os

client = OpenAI(
  api_key=os.getenv('VSEGPT_API_KEY'), # ваш ключ в VseGPT после регистрации
  base_url="https://api.vsegpt.ru/v1",
)

def release_text_to_desc(release_text):
  system_text = """
  Ты анализируешь текст документов, связанных с выпуском цифровых финансовых активов (ЦФА). Твоя задача — извлечь ключевые данные и вернуть их в формате JSON с фиксированными названиями полей. Структура ответа должна быть следующей:
  {
    "cfa_count": "",
    "cfa_price": "",
    "coupon_period": "",
    "date_time_placement_start": "",
    "date_time_placement_end": "",
    "cfa_repayment_date_time": "",
    "cfa_repayment_method": "",
  }

  Пояснения к полям и их формат:
  "cfa_count" — количество выпущенных ЦФА как целое число (например, "100000").
  "cfa_price" — цена одного ЦФА с указанием валюты в формате: ЧЧЧЧ.ВВВ [единица измерения] (например, "1000.00 руб").
  "coupon_period" — период выплаты купонов в формате: каждый N [еденица времени] (например, "каждые 6 месяцев" для периода 6 месяцев или "каждый 1 месяц" для периода месяц).
  "date_time_placement_start" — дата и время начала размещения ЦФА в формате: ДД.ММ.ГГГГ ЧЧ:ММ МСК (например, "04.09.2024 09:00 МСК").
  "date_time_placement_end" — дата и время окончания размещения ЦФА в формате: ДД.ММ.ГГГГ ЧЧ:ММ МСК (например, "05.09.2024 18:00 МСК").
  "cfa_repayment_date_time" — дата и время погошения ЦФА в формате: ДД.ММ.ГГГГ ЧЧ:ММ МСК (например, "05.09.2024 18:00 МСК").
  "cfa_repayment_method" — способ погашения ЦФА в свободном формате. Не больше обного предложения.

  Если какая-то информация отсутствует, оставь соответствующее поле пустым.
  Всегда возвращай результат в формате JSON с указанными полями и заданными форматами.
  Используй исключительно json разметку в ответе, ничего больше.
  """

  messages = []
  messages.append({"role": "system", "content": system_text})
  messages.append({"role": "user", "content": release_text})

  response_big = client.chat.completions.create(
      model="openai/gpt-4o-mini", # id модели из списка моделей - можно использовать OpenAI, Anthropic и пр. меняя только этот параметр
      messages=messages,
      temperature=1,
      n=1,
      max_tokens=3000, # максимальное число ВЫХОДНЫХ токенов. Для большинства моделей не должно превышать 4096
      #extra_headers={ "X-Title": "My App" }, # опционально - передача информация об источнике API-вызова
  )
  response = response_big.choices[0].message.content
  if response:
    response = response.replace("```json", "").replace("```", "")
  print('raw', response)
  try:
    import json
    response = json.loads(response)
  except Exception as error:
    print(error)
    response = None
  return response


