from flaskapp import bot_methods, app
from config.secrets import HOST

if __name__ == "__main__":
    bot_methods.remove_webhook()
    bot_methods.set_webhook(HOST)
    app.run(debug=True, port=5000)
