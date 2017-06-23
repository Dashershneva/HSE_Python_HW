import telebot
import flask
import random
import re
import conf

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN, threaded=False)
bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app = flask.Flask(__name__)

bot.remove_webhook()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Привет, я бот, и я люблю перемешивать буквы в словах")

@bot.message_handler(func=lambda m: True) # здесь описываем, на какие сообщения реагирует функция
def my_function(message):
    reg = '\W'
    text = str(message.text)
    text_lowered = text.lower()
    text_clean = re.sub(u"\W", ' ', text_lowered)
    text_clean = text_clean.replace('  ', ' ')
    word_shuffled = []
    words = text_clean.split(' ')
    for word in words:
        symbol_list = []
        for symbol in word:
            symbol_list.append(symbol)
        text_shuffle = random.shuffle(symbol_list)
        word_shuffled.append(''.join(symbol_list))
    if text[0].isupper():
        new_text = ''.join(word_shuffled)
        i = 0
        for letter in text:
            if re.search(reg, letter):
                new_text = new_text[:i] + letter + new_text[i:]
            i += 1
        reply = new_text[0].upper() + new_text[1:]
    else:
        new_text = ''.join(word_shuffled)
        i = 0
        for letter in text:
            if re.search(reg, letter):
                new_text = new_text[:i] + letter + new_text[i:]
            i += 1
        reply = new_text
    bot.send_message(message.chat.id, reply)

@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)