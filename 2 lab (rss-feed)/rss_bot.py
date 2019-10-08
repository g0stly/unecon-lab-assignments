import telebot

token = '980878523:AAEUYxMijMvEJTuS55crcbQc10JLbF_ApM4'
bot = telebot.TeleBot(token)

last_click = None

# стартовая клавиатура
start_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
start_keyboard.row('Выбрать категорию', 'Выбрать ключевые слова')
start_keyboard.row('Добавить собственный источник')
start_keyboard.row('Выход')


@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    global start_keyboard

    bot.send_message(message.chat.id,
                     'Привет!  :)\n\n' +
                     'Поздравляю, ты был экспериментально выбран для тестирования ' +
                     'новой адаптивной системы подбора новостей.\n\nВот, что я пока что умею:\n' +
                     '✔ подбирать новости из установленных источников\n' +
                     '✔ добавлять твои собственные источники\n\n\n' +
                     '🎲 вопросы/предложения пишите сюда:  @g0stly', reply_markup=start_keyboard)

    #record_data('id', message.from_user.id)


@bot.message_handler(content_types=['text'])
def send_message(message):
    global last_click, start_keyboard

    # клавиатура с выбором категорий
    categories_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    categories_markup.row('Политика', 'Спорт')
    categories_markup.row('Наука', 'Искусство')
    categories_markup.row('Отмена')

    # клавиатура общего назначения
    cancel_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    cancel_markup.row('Отмена')

    if message.text == 'Выход':
        bot.send_message(message.chat.id, 'На сегодня, похоже, хватит новостей')

    elif message.text == 'Выбрать категорию':
        last_click = 'choose category'
        bot.send_message(message.chat.id, 'Выбери что-нибудь из этого:', reply_markup=categories_markup)

    elif message.text == 'Выбрать ключевые слова':
        last_click = 'choose keywords'
        bot.send_message(message.chat.id, 'Введите ключевые слова через запятую:', reply_markup=cancel_markup)

    elif message.text == 'Отмена':
        if last_click == 'choose category':
            bot.send_message(message.chat.id, 'Вы отменили выбор категории. Выберите дальнейшее действие.',
                             reply_markup=start_keyboard)
        elif last_click == 'choose keywords':
            bot.send_message(message.chat.id, 'Вы отменили выбор ключевых слов. Выберите дальнейшее действие.',
                             reply_markup=start_keyboard)

    #elif message.text in ['Политика', 'Спорт', 'Наука', 'Искусство']:
    #    record_data('categories', message.text, message.chat.id)

    else:
        bot.send_message(message.chat.id, message.text)
        print(message.text)


def record_data(cat, data, ident=None):
    import json

    with open('data_file.json', 'r') as read_obj:
        current = json.load(read_obj)
        if cat == 'id':
            current['users'][data] = {"categories": [], "keywords": []}
        else:
            current['users'][str(ident)][cat].append(data)

    with open('data_file.json', 'w') as write_obj:
        json.dump(current, write_obj, ensure_ascii=False)


bot.polling()
