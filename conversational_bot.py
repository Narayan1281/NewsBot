import logging
from flask import Flask, request
from telegram import ForceReply, Update, Bot, ReplyKeyboardMarkup, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher
from utils import fetch_news, get_reply, topics_keyboard

#enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# telegram bot token
TOKEN = "5572041133:AAHaM0BCWxWpxDDOXeaX90bZhj3uWTcj2wY"

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello"

@app.route(f'/{TOKEN}',methods=['GET', 'POST'])
def webhook():
    """webhook view which receives updates from telegram"""
    # create update object from json-format request data
    # just for verifying if our webhook application is working or not
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

def news(update, context):
    """Creating a keyboard Markup"""
    context.bot.send_message(chat_id=update.message.chat_id, text="Choose a category", reply_markup = ReplyKeyboardMarkup(keyboard= topics_keyboard ,one_time_keyboard=True))
    # context.bot.send_message(chat_id=update.message.chat_id, text="Choose a category", 
    # reply_markup = InlineKeyboardMarkup(keyboard= topics_keyboard))


# def echo_text(update, context):
#     """callback function for text message handler"""
#     reply = update.message.text
#     context.bot.send_message(chat_id=update.message.chat_id, text=reply)

# ################### We are replacing echo_text function with reply_text in 
# ################### order to make our bot conversational
def reply_text(update, context):
    intent, reply = get_reply(update.message.text, update.message.chat_id)
    if intent == "get_news" :
        # reply_message = "{}".format(reply)
        # context.bot.send_message(chat_id=update.message.chat_id, text = reply_message)
        articles = fetch_news(reply)
        if len(articles) == 0:
            context.bot.send_message(chat_id=update.message.chat_id, text = "Sorry! Currently we are unable to find news in this category. Try another!")
        for article in articles :
            context.bot.send_message(chat_id=update.message.chat_id, text = article['link'])
    else:
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
    bot.set_webhook("https://493b-2401-4900-43ac-2839-4460-c1fc-c731-5def.in.ngrok.io/" + TOKEN)
    dp = Dispatcher(bot, None)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", _help))
    dp.add_handler(CommandHandler("news", news))
    dp.add_handler(MessageHandler(Filters.text, reply_text))
    dp.add_handler(MessageHandler(Filters.sticker, echo_sticker))
    dp.add_error_handler(error)
    app.run(port=8443)