
import os
from flask import request, Response
from flaskapp import app, bot_methods
from view.Menus import questions_keyboard, admins_contact, answers, enter_name_keyboard

bot_name = "asazoonbot"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        bot_methods.send_message(msg, 112042461)
        is_text = text_check(msg)
        if is_text:
            chat_id = msg['message']['chat']['id']
            if is_text == "/start":
                greeting(msg)
            elif is_text == "/registration":
                registration(chat_id)
            elif is_text == "/link":
                store_links(chat_id)
            elif is_text == "/contacts":
                contact(chat_id)
            elif is_text == "/question":
                questions(chat_id)

            user_path = os.path.join(
                "/home/Nb72/dorfak-bot/users", str(chat_id)+".txt")
            if os.path.exists(user_path):
                phone_number_check(msg)
                check_name(msg)

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


def registration(chat_id):
    user_path = os.path.join(
        "/home/Nb72/dorfak-bot/users", str(chat_id)+".txt")
    if not os.path.exists(user_path):
        with open(user_path, "w", encoding="utf-8") as file:
            file.write(str(chat_id)+"\n0")
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


def phone_number_check(msg):
    number = msg['message']['text']
    chat_id = msg['message']['chat']['id']
    user_path = os.path.join(
        "/home/Nb72/dorfak-bot/users", str(chat_id)+".txt")
    if number.isnumeric():
        if len(number) == 11 and number[0] == "0":
            is_in_file = False
            with open(user_path, "r", encoding="utf-8") as file:
                for line in file:
                    if number in line:
                        is_in_file = True
                        break
            if not is_in_file:
                path = f"/home/Nb72/dorfak-bot/users/{chat_id}.txt"
                update_info(path, 1, f"{number}\n0")
                inline_keyboard = enter_name_keyboard
                bot_methods.send_message_with_keyboard(
                    "دکمه زیر را فشرده و نام و نام خانوادگی خود را وارد نمایید.", chat_id, inline_keyboard)
            else:
                bot_methods.send_message(
                    "شماره تلفن همراه شما قبلا ثبت شده است.\n لطفا نام و نام خانوادگی خود را به شکل زیر وارد نمایید.\n نمونه نام: \n <علی_احمدی>", chat_id)
        else:
            bot_methods.send_message(
                "شماره ای که وارد کرده اید نادرست است لطفا شماره تلفن همراه خود را به صورت صحیح وارد کنید\n مانند نمونه زیر\n نمونه: 09123456789", chat_id)


def check_name(msg):
    name = msg['message']['text']
    chat_id = msg['message']['chat']['id']
    path = os.path.join(
        "/home/Nb72/dorfak-bot/users", str(chat_id)+".txt")
    if f"@{bot_name} /Name:" in name:
        name = name.replace(f"@{bot_name} /Name:", "")
        update_info(path, 2, f"{name}")
        bot_methods.send_message(
            "نام و نام خانوادگی شما با موفقیت ثبت کردید.", chat_id)
        with open(path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        info = ""
        for item in lines:
            info += item.replace("\n", "")
            info += "\n"
        bot_methods.send_message(
            f"شما با اطلاعات زیر در آسازون ثبت نام شدید:\n{info}", chat_id)
        bot_methods.forward_message("{info}", "-1001971910516", 5250278182)


def update_info(file_path, line_number, new_data):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        lines[line_number] = new_data+"\n"

    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(lines)
