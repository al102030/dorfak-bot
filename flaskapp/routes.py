from flask import request, Response
from flaskapp import app, bot_methods
from view.Menus import questions_keyboard


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        is_text = text_check(msg)
        if is_text:
            bot_methods.send_message(msg, "112042461")
            chat_id = msg['message']['chat']['id']
            if is_text == "/start":
                greeting(msg)
            elif is_text == "/enroll":
                pass
            elif is_text == "/link":
                pass
            elif is_text == "/contacts":
                pass
            elif is_text == "/question":
                questions(chat_id)
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
    chat_id = msg['message']['chat']['id']
    greet = "در خدمت شما هستم برای شروع از منوی زیر استفاده نمایید."
    bot_methods.send_message(greet, chat_id)


def enroll():
    pass


def store_links():
    pass


def contact():
    pass


def questions(chat_id):
    inline_keyboard = questions_keyboard
    bot_methods.send_message_with_keyboard(
        "سوالات پرتکرار کاربران",
        chat_id, inline_keyboard)