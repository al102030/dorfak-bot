from flask import Flask
from config.secrets import TOKEN
from bot.Telegram import Telegram


app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'd2bc111a99a637fde34d102f184eebf2'
bot_methods = Telegram(TOKEN)

from flaskapp import routes  # noqa: E402
