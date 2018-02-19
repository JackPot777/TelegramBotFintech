import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


# Import project modules
import messages.texthandlers as tf
import messages.userfunctions as uf
import messages.photohandlers as pf
import utils.logs as logs
import configuration.private as private

# Don't forget to delete Token before commit!
# It is a private key used to connect to bot
TOKEN = private.TOKEN_DEV

bot = telegram.Bot(token=TOKEN)

def main():
    # Create updater and pass it bot's token
    updater = Updater(token=TOKEN)

    # Get dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Command Handlers Initialisation
    startHandler = CommandHandler('start', uf.start) # Working
    getC3POHandler = CommandHandler('C-3PO', uf.getC3PO) # Working
    getAdminsHandler = CommandHandler('admins', uf.getAdmins) # error "There is no administrators in the private chat"
    getAnswerHandler = CommandHandler('answer', uf.getAnswer) # Working

    # Text Handlers Initialisation
    echoHandler = MessageHandler(Filters.text, tf.echo) # Working

    # Photo Handlers Initialisation
    photoDownloadHandler = MessageHandler(Filters.photo, pf.downloadPhoto) # Working

    dispatcher.add_error_handler(logs.error)

    # Adding Command Handlers
    dispatcher.add_handler(startHandler)
    dispatcher.add_handler(getC3POHandler)
    #dispatcher.add_handler(getAdminsHandler)
    dispatcher.add_handler(getAnswerHandler)

    # Adding Text Handlers
    dispatcher.add_handler(echoHandler)

    # Adding Photo Handlers
    dispatcher.add_handler(photoDownloadHandler)

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl+C or terminate it any other way
    updater.idle()


if __name__ == '__main__':
    main()
