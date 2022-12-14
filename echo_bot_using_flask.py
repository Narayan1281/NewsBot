import logging
from flask import Flask, request
from telegram import ForceReply, Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher

#enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# telegram bot token
TOKEN = "Add Token of your bot here"

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello"

@app.route(f'/{TOKEN}',methods=['GET', 'POST'])
def webhook():
    """webhook view which receives updates from telegram"""
    # create update object from json-format request data
    update = Update.de_json(request.get_json(),bot)
    # process update
    dp.process_update(update)
    return "ok"


def start(update, context):
    """Callback function for /start handler"""
    author = update.message.from_user.first_name + " " + update.message.from_user.last_name
    reply = "Hi! {}".format(author)
    context.bot.send_message(chat_id=update.message.chat_id, text=reply)

def _help(update, context):
    """callback function for /help handler"""
    help_txt = "Hey! This is a help text."
    context.bot.send_message(chat_id=update.message.chat_id, text=help_txt)

def echo_text(update, context):
    """callback function for text message handler"""
    reply = update.message.text
    context.bot.send_message(chat_id=update.message.chat_id, text=reply)

def echo_sticker(update, context):
    """callback function for sticker message handler"""
    context.bot.send_sticker(chat_id=update.message.chat_id, sticker=update.message.sticker.file_id)

def error(update, context):
    """callback function for error handler"""
    logger.error("Update '%s' caused error '%s' ", update, context.error)



# def main():
    # updater = Updater(TOKEN) ## we don't need to do polling
    # dp = updater.dispatcher #Dispatcher

   

    

    # updater.start_polling()
    # logger.info("Started polling ...")
    # updater.idle()


if __name__ == "__main__":
    # main()

    bot = Bot(TOKEN)
    bot.set_webhook("https://0117-2409-4056-e1d-1de6-51bb-235d-c34e-da50.in.ngrok.io/" + TOKEN)
    dp = Dispatcher(bot, None)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", _help))
    dp.add_handler(MessageHandler(Filters.text, echo_text))
    dp.add_handler(MessageHandler(Filters.sticker, echo_sticker))
    dp.add_error_handler(error)
    app.run(port=8443)