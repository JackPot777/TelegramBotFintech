import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters

from utils.S3 import S3Instance
from database.UserTableClass import UserTable
from database.PicturesTableClass import PicturesTable

# Import project modules
import database.pictures

import messages.texthandlers as tf
import messages.photohandlers as pf
from actions import userfunctions as uf
from actions import adminfunctions as admin
import utils.logs as logs
import configuration.private as private
import configuration.public as public


# CONFIGURATION
# Private key used to connect to bot
TOKEN = private.TOKEN_PROM

admin_auto_login = True # Enable admin functions for user in admin list without logging in
database_reload = True # Delete and create Databases before start of bot
S3_reload = True # Deletes and create S3 Bucket before start of bot

bot = telegram.Bot(token=TOKEN)

def main():

    # Classes Initialization
    S3 = S3Instance()
    userTableInstance = UserTable()
    picturesTableInstance = PicturesTable()

    # Refresh Tables in DataBase
    if database_reload:
        userTableInstance.drop()
        userTableInstance.create()
        picturesTableInstance.drop()
        picturesTableInstance.create()

    # Refresh s3 Bucket
    if S3_reload:
        S3.deleteFilesInS3Bucket()

    # Create updater and pass it bot's token
    updater = Updater(token=TOKEN)

    # Get dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Command Handlers Initialisation
    startHandler = CommandHandler('start', uf.start) # Working
    getC3POHandler = CommandHandler('C-3PO', uf.getC3PO) # Working
    getAnswerHandler = CommandHandler('answer', uf.getAnswer) # Working

    getUserNameHandler = CommandHandler('myname', uf.getMyUserName) # Working
    getUserIDHandler = CommandHandler('myid', uf.getMyId) # Working

    getSecretLinkHandler = CommandHandler('getlink', uf.getLink, pass_args=True) # Working

    getLastPicture = CommandHandler('lastpicture', uf.getMyLastPicture) # Working
    getPicturebyID = CommandHandler('picture', uf.getPictyreByID, pass_args=True) # Working
    updatePictureName = CommandHandler('rename', uf.updateName, pass_args=True) # Working
    setPublic = CommandHandler('setpublic', uf.setPublic, pass_args=True)
    delelePicturebyID = CommandHandler('delete', uf.deletePictureByID, pass_args=True) # Working
    getListofPictures = CommandHandler('pictureslist', uf.getUserPictures)
    getOwnerofPicture = CommandHandler('owner', uf.getOwnerOfPicture, pass_args=True) # Working
    getMyPictures = CommandHandler('pictures', uf.getAllMyPictures)

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

    dispatcher.add_handler(getLastPicture)
    dispatcher.add_handler(getPicturebyID)
    dispatcher.add_handler(setPublic)
    dispatcher.add_handler(updatePictureName)
    dispatcher.add_handler(delelePicturebyID)
    dispatcher.add_handler(getListofPictures)
    dispatcher.add_handler(getMyPictures)
    dispatcher.add_handler(getOwnerofPicture)

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
