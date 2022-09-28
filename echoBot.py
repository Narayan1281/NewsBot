import logging
from telegram import ForceReply, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

#enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# telegram bot token
TOKEN = "5572041133:AAHaM0BCWxWpxDDOXeaX90bZhj3uWTcj2wY"

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



def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher #Dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", _help))
    dp.add_handler(MessageHandler(Filters.text, echo_text))
    dp.add_handler(MessageHandler(Filters.sticker, echo_sticker))
    dp.add_error_handler(error)

    updater.start_polling()
    logger.info("Started polling ...")
    updater.idle()


if __name__ == "__main__":
    main()