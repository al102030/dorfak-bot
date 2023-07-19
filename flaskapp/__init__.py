from flask import Flask
from config.secrets import TOKEN
from bot.Telegram import Telegram


app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = '4edc0281f3899c05d40adf12a1102fef'
bot_methods = Telegram(TOKEN)
