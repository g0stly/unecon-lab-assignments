import telebot
import json
import time
from decoration import *
from configuration import *
from processing import *

token = ''
bot = telebot.TeleBot(token)

wait_for_category = False
wait_for_keywords = False
del_categories = False
del_keywords = False
last_joke = ''


# стартовое сообщение
@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    global start_kbrd
    global wait_for_category, wait_for_keywords, del_categories, del_keywords

    bot.send_message(message.chat.id, start_msg,
                     reply_markup=start_kbrd)
    wait_for_category = False
    wait_for_keywords = False
    del_categories = False
    del_keywords = False

    # добавление нового пользователя в json-файл
    add_user(message.from_user.id)


@bot.message_handler(commands=['sources', 'links'])
def show_links(message):
    global start_kbrd
    with open('rss_bot_info.json', 'r') as file:
        info = json.load(file)['sources']
    links = []
    for category in info:
        links.extend(['<b>' + category + '</b>'] + info[category])

    bot.send_message(message.chat.id, 'Вот ссылки, которые у меня сейчас есть:\n' + '\n'.join(links),
                     parse_mode='HTML', reply_markup=start_kbrd)


# обработчик входящих сообщений
@bot.message_handler(content_types=['text'])
def send_message(message):
    global start_kbrd, pref_kbrd, categories_kbrd, cancel_kbrd
    global wait_for_category, wait_for_keywords, del_categories, del_keywords

    if message.text == '📟 Мой профиль':
        with open('rss_bot_info.json', 'r') as file:
            info = json.load(file)['users']
            _id = str(message.from_user.id)

            if _id in info.keys():
                bot.send_message(message.chat.id,
                                 f'ваш id:  {_id}' + f'\nкатегории:  {convert(info[_id]["categories"])}' +
                                 f'\nключевые слова:  {convert(info[_id]["keywords"])}', reply_markup=pref_kbrd)
            else:
                add_user(message.from_user.id)
                bot.send_message(message.chat.id,
                                 f'ваш id:  {_id}' + f'\nкатегории:  {convert(info[_id]["categories"])}' +
                                 f'\nключевые слова:  {convert(info[_id]["keywords"])}', reply_markup=pref_kbrd)

    elif message.text == '🗣 Новости':
        bot.send_message(message.chat.id, 'оставайтесь на линии.\nзапрос обрабатывается.')
        result = get_news(message.from_user.id)
        if result == 0:
            time.sleep(2)
            bot.send_message(message.chat.id, 'кажется, ты не выбрали никакую категорию.\nвыбери, пожалуйста.',
                             reply_markup=categories_kbrd)
            wait_for_category = True
        else:
            feed, info = result
            if not feed:
                bot.send_message(message.chat.id, 'к сожалению, я ничего не нарыл(', reply_markup=start_kbrd)
            else:
                bot.send_message(message.chat.id, f'фух, я отсмотрел {info[1]} новостей за {round(info[0], 2)} сек.')
                for news in feed:
                    bot.send_message(message.chat.id, reformat(news), parse_mode='HTML')
                    time.sleep(5)
                bot.send_message(message.chat.id, 'ну как тебе? пойдет?', reply_markup=start_kbrd)

    elif message.text == '🤪 Анекдот':
        bot.send_message(message.chat.id, random_joke(), reply_markup=start_kbrd)

    elif message.text == '+ категория':
        wait_for_category = True
        bot.send_message(message.chat.id, 'выбери категорию.', reply_markup=categories_kbrd)

    elif message.text == '+ ключ. слова':
        wait_for_keywords = True
        bot.send_message(message.chat.id, 'введи ключевые слова через запятую.', reply_markup=cancel_kbrd)

    elif message.text == '- категория':
        del_categories = True
        bot.send_message(message.chat.id, 'от каких категорий ты хочешь отписаться?\nнапиши через запятую.')

    elif message.text == '- ключ. слова':
        del_keywords = True
        bot.send_message(message.chat.id, 'какие ключевые слова ты хочешь удалить?\nнапиши через запятую.')

    elif message.text == 'отмена':
        wait_for_category = False
        wait_for_keywords = False
        del_categories = False
        del_keywords = False
        bot.send_message(message.chat.id, 'что прикажешь делать дальше?', reply_markup=start_kbrd)

    elif message.text.startswith('/newsource'):
        ans = add_source(message.text[10:])
        if ans == 1:
            bot.send_message(message.chat.id, 'новая лента добавлена.')
        else:
            bot.send_message(message.chat.id, 'какие-то временные технические шоколадки с добавлением твоей ленты')
    else:

        if wait_for_category:
            add_preferences(message.from_user.id, 'categories', message.text)
            bot.send_message(message.chat.id, 'профиль обновлен.\nхочешь выбрать еще?', reply_markup=categories_kbrd)

        elif wait_for_keywords:
            add_preferences(message.from_user.id, 'keywords', message.text)
            bot.send_message(message.chat.id, 'профиль обновлен.', reply_markup=start_kbrd)
            wait_for_keywords = False

        elif del_categories:
            del_preferences(message.from_user.id, 'categories', message.text)
            bot.send_message(message.chat.id, 'профиль обновлен.', reply_markup=start_kbrd)
            del_categories = False

        elif del_keywords:
            del_preferences(message.from_user.id, 'keywords', message.text)
            bot.send_message(message.chat.id, 'профиль обновлен.', reply_markup=start_kbrd)
            del_keywords = False


bot.polling(none_stop=True)
