from flask import request, Response
from flaskapp import app, bot_methods


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        # chat_id = msg['message']['chat']['id']
        if text_check(msg)
        greeting(msg)
        return Response('ok', status=200)
    else:
        return '<h1>Asazoon Telegram Bot</h1>'


def text_check(msg):
    try:
        is_text = msg['message']['text']
    except KeyError as error:
        print("Text not found", error)
        is_text = None
    return is_text


def greeting(msg):
    text = msg['message']['text']
    chat_id = msg['message']['chat']['id']
    greet = "در خدمت شما هستم برای شروع از منوی زیر استفاده نمایید."
    if text is "/start":
        bot_methods.send_message(msg, chat_id)
