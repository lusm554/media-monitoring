import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from concurrent.futures import ThreadPoolExecutor

# Загружаем модель и токенизатор
model_name = "IlyaGusev/rugpt3medium_sum_gazeta"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Перенос модели на GPU (если доступен)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# Функция для генерации краткого содержания нескольких статей (batch processing)
def generate_summaries_batch(article_texts):
    # Токенизация каждого текста
    tokenized_inputs = tokenizer(
        article_texts,
        max_length=600,
        add_special_tokens=False, 
        padding=True,   # Padding для batch обработки
        truncation=True,
        return_tensors="pt"  # Возвращаем тензоры для работы с моделью
    )

    input_ids = tokenized_inputs["input_ids"].to(device)

    # Генерация результатов без вычисления градиентов
    with torch.no_grad():
        output_ids = model.generate(
            input_ids=input_ids,
            no_repeat_ngram_size=4,
            num_return_sequences=1  # Количество возвращаемых последовательностей
        )

    # Декодирование и обработка результатов
    summaries = []
    for output in output_ids:
        summary = tokenizer.decode(output, skip_special_tokens=False)
        summary = summary.split(tokenizer.sep_token)[1]
        summary = summary.split(tokenizer.eos_token)[0]
        summaries.append(summary)

    return summaries


# Параллельная обработка статей с batch processing
def process_articles_in_batches(articles, batch_size=4, max_workers=4):
    def batch_generator(lst, batch_size):
        for i in range(0, len(lst), batch_size):
            yield lst[i:i + batch_size]

    summaries = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Обрабатываем данные батчами
        futures = [executor.submit(generate_summaries_batch, batch) for batch in batch_generator(articles, batch_size)]
        for future in futures:
            summaries.extend(future.result())
    return summaries



import sys; sys.path.insert(0, '.')
import scraper_lib

articles = scraper_lib.CfaAllNewsScraper(error='raise').fetch_and_parse(scraper_lib.Periods.LAST_24_HOURS)
# Пример списка текстов
article_texts = [x.body_text for x in articles if x]

# Обработка текстов батчами
summaries = process_articles_in_batches(article_texts, batch_size=4, max_workers=4)

# Вывод результатов
for summary in summaries:
    print(summary)

