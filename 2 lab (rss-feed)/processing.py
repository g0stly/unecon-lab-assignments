import feedparser
import random
import time
import json
import pymorphy2
import nltk
from nltk.corpus import stopwords
import re


# рандомный анекдот
def random_joke():
    global last_joke

    link = 'http://www.jokesoftheday.net/jokes-feed/'
    jokes = feedparser.parse(link).entries
    ans = jokes[random.randint(0, len(jokes) - 1)].summary

    while len(ans.split()) > 50 and ans != last_joke:
        ans = jokes[random.randint(0, len(jokes) - 1)].summary
        ans = ans[:ans.index('Read more on') - 1]
    last_joke = ans

    return cleanhtml(last_joke)


# анализ новостей из пользовательских категорий по пользовательским ключевым словам
def get_news(user_id):
    with open('rss_bot_info.json', 'r') as read_obj:
        current = json.load(read_obj)

    start_time = time.time()
    chosen_news = []
    user_id = str(user_id)
    news_viewed = 0

    # запоминание пользовательских предпочтений
    try:
        categories = current['users'][user_id]['categories']
        keywords = current['users'][user_id]['keywords']
        links = [item for sublist in [current['sources'][x] for x in categories] for item in sublist]
    except:
        return -1

    if links:
        # анализ каждой новости из каждой ссылки
        for link in links:
            news_line = feedparser.parse(link).entries
            for news in news_line:

                news_viewed += 1
                content = cleanhtml(news.summary)
                # проверка валидности новости
                if check_it(content, keywords):

                    if 'document.write' in content:
                        content = content[: content.index('document.write') - 1]
                    clean = {'title': news.title, 'link': news.links[0]['href'], 'content': content}
                    chosen_news.append(clean)
                if len(chosen_news) == 7:
                    break
    else:
        return 0

    return [chosen_news, [time.time() - start_time, news_viewed]]


# проверка новости на содержание ключевых слов
def check_it(text, keywords):
    morph = pymorphy2.MorphAnalyzer()

    if keywords:
        keywords = set([morph.parse(word.lower())[0].normal_form for word in keywords])
        word_list = set([morph.parse(i.lower())[0].normal_form for i in nltk.word_tokenize(text) \
                         if i not in '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~»«–' and i not in stopwords.words('russian')])

        return keywords & word_list != set()

    else:
        return True


# очистка самой новости от тэгов и прочего мусора
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', raw_html)
    return ' '.join(cleantext.split())


# форматирование словаря - новости
def reformat(text):
    return '<b>' + text['title'] + '</b>' + '\n\n' + text['content'] + '\n\n' + text['link']


# маленькая вспомогательная функция
def convert(data):
    if not data:
        return '-'
    else:
        return ', '.join(data)
