import re
from flask import Flask
from flask import request
from flask.views import MethodView
import requests
import os
from dotenv import load_dotenv
from pyshorteners.shorteners import tinyurl


short = tinyurl.Shortener()
load_dotenv()

app = Flask(__name__)
API_URL = os.environ.get('API_URL')
TOKEN = os.environ.get('TOKEN')
WEBHOOK = os.environ.get('WEBHOOK')

TELEGRAM_URL = f'http://api.telegram.org/bot{TOKEN}/sendMessage'


def send_message(chat_id, tmp):   # OOOOPPPPPAAAAAAAAAAAAAAAAAAAAAA EMAE
    session = requests.Session()
    message = f'***{tmp}***'
    r = session.get(TELEGRAM_URL, params=dict(chat_id=chat_id, text=message, parse_mode='Markdown'))
    return r


def get_data_from_api(command):
    url = API_URL + command
    session = requests.Session()
    r = session.get(url)
    return r.json()

# http://127.0.0.1:8000/api/v1/vacancies/?city=kiev&language=gdansk
# http://127.0.0.1:8000/api/v1/vacancies/?city=kiev&language=java


def parse_text(text_msg):
    """/start or /help, /city or /language, @gdansk or @python"""
    addresses = {'city': '/cities', 'language': '/languages'}
    command_p = r'/\w+'   # SEARCH IN TEXT 'SYMBOL', SLASH, LITTERS
    dog_p = r'@\w+'
    message = '''
                Invalid request. The request does not comply with the bot rules.
                If you need help and further instructions, enter "/help" (through a slash).
                This is not artificial intelligence, but a telegram bot,
                if you need to communicate with a developed network, follow the link - https://chat.openai.com,
                otherwise enter the commands prepared for you!
               '''
    if '/' in text_msg:
        if '/start' in text_msg or '/help' in text_msg:
            message = '''
                         To find out which cities are available, send `/city` in a message.
                         To find out about available specialties, send `/language`
                         To make a request for saved vacancies, send a message separated by a space - @city @language.
                         For example, like this - `@gdansk @python`
                         Please write down the city and then the vacancy.
                      '''
            return message
        else:
            command = re.search(command_p, text_msg).group().replace('/', '')
            command = addresses.get(command, None)
            return [command] if command else None
    elif text_msg == 'py44':
        return 'Thank you Dima ept!'
    elif '@' in text_msg:
        if str(text_msg).count('+'):
            result = re.findall(dog_p, text_msg)
            result[1] = ('c' + '%2B%2B')
            commands = [s.replace('@', '') for s in result]
        else:
            result = re.findall(dog_p, text_msg)
            commands = [s.replace('@', '') for s in result]
        return commands if len(commands) == 2 else None
    else:
        return message


# KIEV NOT PRINT
class BotAPI(MethodView):
    def get(self):
        return 'GET WORK'

    def post(self):
        resp = request.get_json()
        chat_id = resp["message"]["chat"]["id"]
        text = resp["message"]["text"]
        print(chat_id, text)
        tmp = parse_text(text)
        if tmp:
            if len(tmp) > 10:
                send_message(chat_id, tmp)
            elif len(tmp) == 1:
                resp = get_data_from_api(tmp[0])
                if resp:
                    message = ''
                    for d in resp:
                        message += '#' + d['slug'] + '\n'
                    if tmp[0] == '/language':
                        msg = 'Available languages \n'
                    else:
                        msg = 'Available cities: \n'
                    send_message(chat_id, msg + message)
            elif len(tmp) == 2:
                url = '/vacancies/?city={}&language={}'.format(*tmp)
                # /api/v1/vacancies/?city=kiev&language=java
                resp = get_data_from_api(url)
                print(resp)
                if tmp[0] == 'kiev':   # special processing for urls with 'kiev', since Ukrainian sites had specific urls
                    message = ''
                    for vacancy in resp[:50]:
                        message += '#' + f"{vacancy['title'].strip()}\n {vacancy['company'].strip()}\n"
                        message += f"{short.short(vacancy['url'])}\n\n"
                    msg = f"Available vacancies for city '{tmp[0].title()}' and language '{'C++' if tmp[1] == 'c%2B%2B' else tmp[1].title()}'\n\n"
                    send_message(chat_id, msg + message)
                else:
                    message = ''
                    for vacancy in resp:
                        message += '#' + f"{vacancy['title'].strip()}\n {vacancy['company'].strip()}\n"
                        message += f"{short.short(vacancy['url'])}\n\n"
                    msg = f"Available vacancies for city '{tmp[0].title()}' and language '{'C++' if tmp[1] == 'c%2B%2B' else tmp[1].title()}'\n\n"
                    send_message(chat_id, msg+message)
        return 'GET POST'


app.add_url_rule('/TOKEN/', view_func=BotAPI.as_view('bot'))   # for def not need

if __name__ == '__main__':
    app.run()

# https://api.telegram.org/bot7099495051:AAF6_cuZO-PRwp3PRLUW4eBS-cENN2-lqVo/setWebhook?url=https://184d-2a02-a31b-843c-2600-74ff-5c29-fc68-8bef.ngrok-free.app
# https://api.telegram.org/bot7099495051:AAF6_cuZO-PRwp3PRLUW4eBS-cENN2-lqVo/setWebhook?url=https://de6b-2a02-a31b-843c-2600-7563-d975-792f-1447.ngrok-free.app/TOKEN/

