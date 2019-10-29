import telebot
import json
import feedparser
import re
import random
import nltk
from nltk.corpus import stopwords
import pymorphy2
import time


token = '980878523:AAEUYxMijMvEJTuS55crcbQc10JLbF_ApM4'
bot = telebot.TeleBot(token)
last_click = None

# стартовая клавиатура
start_kbrd = telebot.types.ReplyKeyboardMarkup(True, True)
start_kbrd.row('Новости', 'Анекдот')
start_kbrd.row('Категория', 'Ключевые слова')
start_kbrd.row('Новый источник')
start_kbrd.row('Выход')

# клавиатура с выбором категорий
categories_kbrd = telebot.types.ReplyKeyboardMarkup(True, True)
categories_kbrd.row('Политика', 'Спорт')
categories_kbrd.row('Наука', 'Искусство')
categories_kbrd.row('Отмена')

# клавиатура общего назначения (отмены)
cancel_kbrd = telebot.types.ReplyKeyboardMarkup(True, True)
cancel_kbrd.row('Отмена')


@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    global start_kbrd

    bot.send_message(message.chat.id,
                     'привет!  :)\n\n' +
                     'я тебе каких-нибудь жутко нерелевантных новостей покидаю, ок?', 
                     reply_markup=start_kbrd)
    
    # добавление нового пользователя в json-файл
    add_user(message.from_user.id)
    
    
@bot.message_handler(content_types=['text'])
def send_message(message):
    global start_kbrd, categories_kbrd, cancel_kbrd, last_click
    
    if message.text == 'Новости':
        last_click = None
        bot.send_message(message.chat.id, 'ты сделал запрос на получение новостей.')
        news_all, request_info = get_news(message.from_user.id)
        bot.send_message(message.chat.id, f'фух, я отсмотрел {request_info[1]} новостей за {round(request_info[0], 2)} сек.')
        if news_all != []:
            for news in news_all:
                bot.send_message(message.chat.id, reformat(news), parse_mode='Markdown')
                time.sleep(5)
        else:
            bot.send_message(message.chat.id, 'ничего не нарыл()')
    
    elif message.text == 'Анекдот':
        last_click = None
        bot.send_message(message.chat.id, random_joke())
    
    elif message.text == 'Новый источник':
        last_click = 'add source'
        bot.send_message(message.chat.id, 'введи ссылку на ленту и ее категорию в формате:' +
                        '\n\n[ссылка] [категория]', reply_markup=cancel_kbrd)
    
    elif message.text == 'Категория':
        last_click = 'choose category'
        bot.send_message(message.chat.id, 'выбери что-нибудь из этого: ', reply_markup=categories_kbrd)
    
    elif message.text == 'Ключевые слова':
        last_click = 'choose keywords'
        bot.send_message(message.chat.id, 'введи ключевые слова через запятую.' + '\n\nнапример: конфликт гамбит джокер',
                        reply_markup=cancel_kbrd)
        
    elif message.text == 'Выход':
        last_click = None
        bot.send_message(message.chat.id, '28 новостей на сегодня, ты действовал наверняка, да?')
    
    # обработка перехода к предыдущему шагу
    elif message.text == 'Отмена':
        if last_click == 'choose category':
            bot.send_message(message.chat.id, 'ты отменил выбор категории. \nчто дальше?',
                             reply_markup=start_kbrd)
        elif last_click == 'choose keywords':
            bot.send_message(message.chat.id, 'ты отменил выбор ключевых слов. \nчто дальше?',
                             reply_markup=start_kbrd)
        elif last_click == 'add source':
            bot.send_message(message.chat.id, 'ты отменил добавление нового источника. \nчто дальше?',
                             reply_markup=start_kbrd)
    
    else:
        if last_click == 'add source':
            add_source(message.text)
        elif last_click == 'choose category':
            add_preferences(message.from_user.id, 'categories', message.text)
        elif last_click == 'choose keywords':
            add_preferences(message.from_user.id, 'keywords', message.text)
        elif last_click == None:
            bot.send_message(message.chat.id, 'ты мне какую-то фигню написал (зачем?)')
        
        time.sleep(2)
        bot.send_message(message.chat.id, 'что будем делать дальше?', reply_markup=start_kbrd)
        last_click = None
    
    
# новый пользователь    
def add_user(user_id):
    with open('rss_bot_info.json', 'r') as read_obj:
        current = json.load(read_obj)
        
    if str(user_id) not in list(current['users'].keys()):
        current['users'][str(user_id)] = {"categories": [], "keywords": []}
    
    with open('rss_bot_info.json', 'w') as write_obj:
        json.dump(current, write_obj, ensure_ascii=False)
    
    
# новые предпочтения пользователя (ключевые слова/категория)
def add_preferences(user_id, data_type, data):
    with open('rss_bot_info.json', 'r') as read_obj:
        current = json.load(read_obj)
    
    user_id = str(user_id)
    if data_type == 'categories':
        for word in data.lower().split():
            if word in current['sources'].keys():
                if word not in current['users'][user_id][data_type]:
                    current['users'][user_id][data_type].append(word)
        
    elif data_type == 'keywords':
        for word in data.lower().split():
            if word not in current['users'][user_id][data_type]:
                current['users'][user_id][data_type].append(word)
      
    
    with open('rss_bot_info.json', 'w') as write_obj:
        json.dump(current, write_obj, ensure_ascii=False)
    
    
# новый источник
def add_source(data):
    global bot
    with open('rss_bot_info.json', 'r') as read_obj:
        current = json.load(read_obj)
    
    link, category = data.lower().split()
    
    if link[-3::] == 'xml':
        
        if category in current['sources'].keys():
            if link not in current['sources'][category]:
                current['sources'][category].append(link)
        else:
            current['sources'][category] = [link]

    with open('rss_bot_info.json', 'w') as write_obj:
        json.dump(current, write_obj, ensure_ascii=False)

        
# очистка самой новости от тэгов и прочего мусора
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', raw_html)
    return ' '.join(cleantext.split())


# рандомный анекдот 
def random_joke():
    with open('rss_bot_info.json', 'r') as read_obj:
        current = json.load(read_obj)
        
    link = random.choice(current['sources']['joke'])
    jokes = feedparser.parse(link).entries
    
    try:
        return cleanhtml(jokes[random.randint(0, len(jokes))].summary)
    
    except:
        return('''
        Жила-была курица. И решила она вступить в мафию.
        Пошла курица к самому главному мафиози, к суровому дону, и говорит:
        хочу в мафию! А дон ей отвечает: нет никакой мафии.
        Тогда курица пошла к советнику дона, консильери, и попросила принять
        ее в мафию. Но консильери ответил курице: нет никакой мафии.
        Тогда курица пошла к капитану мафии и попросилась к нему солдатом.
        Но капитан сказал курице: нет никакой мафии.
        Курица загрустила и побрела к себе курятник.
        А там к ней прибежали курицы-подружки и засыпали ее вопросами.
        На все вопросы курица отвечала: нет никакой мафии...
        И тогда все куры поняли, что ее приняли.
        И стали ее бояться.
        ахахах''')

# проверка новости на содержание ключевых слов
def check_it(text, keywords):
    morph = pymorphy2.MorphAnalyzer()
    
    keywords = set([morph.parse(word.lower())[0].normal_form for word in keywords])
    word_list = set([morph.parse(i.lower())[0].normal_form for i in nltk.word_tokenize(text) \
                     if i not in '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~»«–' and i not in stopwords.words('russian')])
    
    return keywords & word_list != set()


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
        return('ошибка данных')
    
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
                if len(chosen_news) == 5:
                    break
                 
    return [chosen_news, [time.time() - start_time, news_viewed]]


# форматирование словаря - новости
def reformat(text):
    return '*' + text['title'] + '*' + '\n\n' + text['content'] + '\n\n' + text['link']

bot.polling()