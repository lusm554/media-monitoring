from openai import OpenAI
import os

def pdf_to_text(pdf_filepath):
	from pdfminer.high_level import extract_text
	import re
	text = extract_text(pdf_filepath)
	text = re.sub(r'\s+', ' ', text) 
	text = re.sub(r'[^\w\s.,!?-]', '', text)
	print(len(text))
	return text

client = OpenAI(
    api_key=os.getenv('VSEGPT_API_KEY'), # ваш ключ в VseGPT после регистрации
    base_url="https://api.vsegpt.ru/v1",
)

def get_release_desc(prompt):
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
	"coupon_period" — период выплаты купонов в формате: каждые N [еденица времени] (например, "кажддые 6 месяцев" для периода 6 месяцев).
	"date_time_placement_start" — дата и время начала размещения ЦФА в формате: ДД.ММ.ГГГГ ЧЧ:ММ МСК (например, "04.09.2024 09:00 МСК").
	"date_time_placement_end" — дата и время окончания размещения ЦФА в формате: ДД.ММ.ГГГГ ЧЧ:ММ МСК (например, "05.09.2024 18:00 МСК").
	"cfa_repayment_date_time" — дата и время погошения ЦФА в формате: ДД.ММ.ГГГГ ЧЧ:ММ МСК (например, "05.09.2024 18:00 МСК").
	"cfa_repayment_method" — способ погашения ЦФА в свободном формате. Не больше обного предложения.

	Если какая-то информация отсутствует, оставь соответствующее поле пустым.
  Всегда возвращай результат в формате JSON с указанными полями и заданными форматами.
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

for path in (f'{i}.pdf' for i in range(1,8)):
	prompt = pdf_to_text(path)
	desc = get_release_desc(prompt)
	print(path)
	print(desc)

