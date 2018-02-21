import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters


# Import project modules
import messages.texthandlers as tf
import messages.photohandlers as pf
from actions import userfunctions as uf
from actions import adminfunctions as admin
import utils.logs as logs
import configuration.private as private

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
    getAnswerHandler = CommandHandler('answer', uf.getAnswer) # Working
    getUserNameHandler = CommandHandler('myname', uf.getMyUserName) # Returns null for me
    getUserIDHandler = CommandHandler('myid', uf.getMyId) # Working
    getSecretLinkHandler = CommandHandler('getlink', uf.getLink, pass_args=True) # Working

    # Admin Command Handlers Initialisation
    adminLoginHandler = CommandHandler('login', admin.login, pass_args=True) # Working
    adminLogoutHandler = CommandHandler('logout', admin.logout) # Working
    adminStatusHandler = CommandHandler('logstatus', admin.loginStatus) # Working
    adminLoggedListHandler = CommandHandler('adminsonline', admin.loginedAdmins) # 'list' object is not callable

    # Text Handlers Initialisation
    echoHandler = MessageHandler(Filters.text, tf.echo) # Working

    # Photo Handlers Initialisation
    photoDownloadHandler = MessageHandler(Filters.photo, pf.downloadPhoto) # Working

    # Error Handler Initialisation
    dispatcher.add_error_handler(logs.error)

    # Adding Command Handlers
    dispatcher.add_handler(startHandler)
    dispatcher.add_handler(getC3POHandler)
    dispatcher.add_handler(getAnswerHandler)
    dispatcher.add_handler(getUserNameHandler)
    dispatcher.add_handler(getUserIDHandler)

    dispatcher.add_handler(getSecretLinkHandler)
    dispatcher.add_handler(CallbackQueryHandler(uf.getLinkButton))

    # Adding Admin Command Handlers
    dispatcher.add_handler(adminLoginHandler)
    dispatcher.add_handler(adminLogoutHandler)
    dispatcher.add_handler(adminStatusHandler)
    dispatcher.add_handler(adminLoggedListHandler)

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
