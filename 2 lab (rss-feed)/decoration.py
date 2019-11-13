import telebot

# стартовая клавиатура
start_kbrd = telebot.types.ReplyKeyboardMarkup(True, True)
start_kbrd.row('🗣 Новости', '🤪 Анекдот')
start_kbrd.row('📟 Мой профиль')

# изменить преференции
pref_kbrd = telebot.types.ReplyKeyboardMarkup(True, True)
pref_kbrd.row('+ категория', '- категория')
pref_kbrd.row('+ ключ. слова', '- ключ. слова')
pref_kbrd.row('отмена')

# клавиатура с выбором категорий
categories_kbrd = telebot.types.ReplyKeyboardMarkup(True, True)
categories_kbrd.row('политика', 'спорт')
categories_kbrd.row('наука', 'искусство')
categories_kbrd.row('отмена')

# клавиатура общего назначения (отмены)
cancel_kbrd = telebot.types.ReplyKeyboardMarkup(True, True)
cancel_kbrd.row('отмена')

# приветствие
start_msg = '''
🤙 привет, любитель новостей!
давай я немного введу тебя в курс дела, вот мой скромный функционал:

🔹 подборка новостей, отобранных по твом категориям и ключевым словам (если таковые имеются)
🔹 конфигурация твоего профиля (добавление/удаление категорий, ключевых слов)
🔹 функция 'хочу смеяться 5 минут', она же - выдача случайного анекдота
🔹 функция 'добавить новый ресурс'
    работает так: /newsource [link] [category]
'''
