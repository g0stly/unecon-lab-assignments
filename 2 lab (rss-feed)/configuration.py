import json
import feedparser
from processing import *


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
    data = data.lower()

    if user_id in current['users'].keys():

        if data_type == 'categories':
            if data in current['sources'].keys():
                if data not in current['users'][user_id][data_type]:
                    current['users'][user_id][data_type].append(data)

        elif data_type == 'keywords':
            for word in data.replace(',', '').split():
                if word not in current['users'][user_id][data_type]:
                    current['users'][user_id][data_type].append(word)
    else:
        add_user(user_id)
        add_preferences(user_id, data_type, data)

    with open('rss_bot_info.json', 'w') as write_obj:
        json.dump(current, write_obj, ensure_ascii=False)

    # новый источник


def add_source(data):
    global bot
    link, category = data.lower().split()

    try:
        test_news = cleanhtml(feedparser.parse(link).entries[0].summary)
        if test_news == '':
            return 0
    except:
        return 0

    with open('rss_bot_info.json', 'r') as read_obj:
        current = json.load(read_obj)

    if category in current['sources'].keys():
        if link not in current['sources'][category]:
            current['sources'][category].append(link)
        else:
            return 0
    else:
        current['sources'][category] = [link]

    with open('rss_bot_info.json', 'w') as write_obj:
        json.dump(current, write_obj, ensure_ascii=False)

    return 1


# удалить предпочтения
def del_preferences(user_id, data_type, data):
    with open('rss_bot_info.json', 'r') as read_obj:
        current = json.load(read_obj)

    user_id = str(user_id)
    data = data.lower().replace(',', '').split()

    try:
        current['users'][user_id][data_type] = list(set(current['users'][user_id][data_type]) - set(data))
    except:
        return 'ошибка данных'

    with open('rss_bot_info.json', 'w') as write_obj:
        json.dump(current, write_obj, ensure_ascii=False)
