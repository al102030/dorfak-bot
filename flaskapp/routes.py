
import os
from flask import request, Response
from flaskapp import app, bot_methods
from view.Menus import questions_keyboard, admins_contact, answers


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        is_text = text_check(msg)
        if is_text:
            chat_id = msg['message']['chat']['id']
            if is_text == "/start":
                greeting(msg)
            elif is_text == "/enroll":
                enroll(chat_id)
            elif is_text == "/link":
                store_links(chat_id)
            elif is_text == "/contacts":
                contact(chat_id)
            elif is_text == "/question":
                questions(chat_id)
        elif "callback_query" in msg:
            answers_questions(msg)
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


def enroll(chat_id):
    user_path = os.path.join(
        "/home/Nb72/dorfak-bot/users", str(chat_id)+".txt")
    with open(user_path, "w", encoding="utf-8") as file:
        file.write(chat_id)
    bot_methods.send_message("لطفا شماره همراه خود را وارد نمایید.", chat_id)


def store_links(chat_id):
    link = "benjamin.aszn.ir"
    bot_methods.send_message(link, chat_id)


def contact(chat_id):
    inline_keyboard = admins_contact
    bot_methods.send_message_with_keyboard(
        """
        هلدینگ دیجیتال مارکتینگ آسازون به عنوان اولین سرویس شتابدهنده ی فروش، ارایه دهنده روش هایی موثر برای افزایش فروش است.
        آدرس آسازون: رشت، فاز یک معلم، قبل از استانداری، ساختمان قصر سفید، طبقه 4، واحد7، شرکت ایده پردازان درفک

تلفن: 01333251880
        """,
        chat_id, inline_keyboard)


def questions(chat_id):
    inline_keyboard = questions_keyboard
    bot_methods.send_message_with_keyboard(
        "سوالات پرتکرار کاربران",
        chat_id, inline_keyboard)


def answers_questions(msg):
    # callback_id = msg['callback_query']['id']
    callback_from_id = msg['callback_query']['from']['id']
    callback_data = msg['callback_query']['data']
    for key, value in answers.items():
        if key == callback_data:
            answer = value
            break
    bot_methods.send_message(
        answer, callback_from_id)
    return True
