from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words


LANGUAGE = "russian"
SENTENCES_COUNT = 3

s = """
ВТБ прогнозирует объем рынка ЦФА по итогам года около 400 млрд рублей

По итогам 2024 года объем рынка цифровых финансовых активов (ЦФА) в России приблизится к 400 млрд рублей. Об этом в рамках ВЭФ-2024 в эфире телеканала РБК ТВ заявил член правления ВТБ Виталий Сергейчук.

«Объем рынка ЦФА в 2024 году уже превысил 200 млрд руб. и может достигнуть 400 млрд руб. Этот рынок активно развивается, его доходность уже сейчас зачастую превышает доходность по сопоставимым биржевым инструментам. Поэтому мы видим большой потенциал роста спроса на данный продукт со стороны инвесторов», – рассказал Виталий Сергейчук.

Он также отметил, что для более активного развития рынка ЦФА необходима автоматизация сделок. «Сейчас ограничен инструментарий, доступный физическим лицам. Как только мы переведем форму или возможность инвестирования в ЦФА в привычный для людей интерфейс – приложения брокерские и банковские в телефоне – будет гораздо больше спрос и всплеск интереса со стороны розничного инвестора к данному продукту», – отметил спикер.

Напомним, что в этом году ВТБ первым в России предложил частным инвесторам цифровые финансовые активы, привязанные к стоимости физического квадратного метра в строящемся жилом комплексе hideOUT. Этот инструмент радикально снизил для розничных инвесторов порог входа на рынок инвестиций в премиальную недвижимость. Доходность и защита капитала инвесторов аналогичны приобретению физического метра жилья в этом ЖК.
"""

def get_russian_stopwords():
  with open('nlp/russian_stop_words.txt', 'rt') as f:
    data = f.read()
  return frozenset(w.rstrip() for w in data.splitlines() if w)

parser = PlaintextParser.from_string(s, Tokenizer(LANGUAGE))
summarizer = Summarizer(Stemmer(LANGUAGE))
import nltk
#nltk.download('stopwords')
#summarizer.stop_words = get_stop_words(LANGUAGE)
#summarizer.stop_words = nltk.corpus.stopwords.words('russian')
summarizer.stop_words = get_russian_stopwords()

for sen in summarizer(parser.document, SENTENCES_COUNT):
  print(sen, len(str(sen)))

