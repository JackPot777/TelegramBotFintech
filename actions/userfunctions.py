# -*- coding: utf-8 -*-
"""
File with functions that can be called by any user
To call a function user should type /<function> in chat window

Don't Forget to add function to Command Handler!

"""
import configuration.public as publ
import database.pictures
from configuration.private import PASSWORD_LIST, SECRET_CHANNEL_LINK
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ChatAction
from utils.S3 import S3Instance
from utils.misc import TIME, rm, hasAccess, isPublic, pictureExists


def start(bot, update):
    """Send greetings message"""
    bot.send_message(chat_id=update.message.chat_id,
                     text="Вечер в хату господа")


def getMyUserName(bot, update):
    """Send Username back"""
    user = update.message.from_user
    bot.send_message(chat_id=update.message.chat_id,
                     text=user.first_name)


def getMyId(bot, update):
    """Send User Id back"""
    user = update.message.from_user
    bot.send_message(chat_id=update.message.chat_id,
                     text=user.id)


def getAnswer(bot, update):
    """Send Answer to the Ultimate Question of Life, the Universe, and Everything"""
    bot.send_message(chat_id=update.message.chat_id,
                     text="Answer to the Ultimate Question of Life, the Universe, and Everything is 42")


def getC3PO(bot, update):
    """Send C-3PO pic to chat"""
    bot.send_photo(chat_id=update.message.chat_id,
                   photo="https://lumiere-a.akamaihd.net/v1/images/C-3PO-See-Threepio_68fe125c.jpeg?region=0%2C1%2C1408%2C792&width=768")


def getLink(bot, update, args):
    """Get link to secret channel"""
    userPassword = args[0]
    if userPassword in PASSWORD_LIST:
        keyboard = [[InlineKeyboardButton(text="Link to Secret channel", url=SECRET_CHANNEL_LINK)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(text="Click to join:",reply_markup=reply_markup)
    else:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Неверный пароль")


def getLinkButton(bot, update):
    """Message with button with url leading to secret channel"""
    query = update.callback_query
    bot.edit_message_text(text="Button",
                          chat_id=query.message.chat_id,
                          parse_mode= "HTML",
                          message_id=query.message.message_id)


def getMyLastPicture(bot, update):
    """Retrieve last photo from database belonging to user and send it back to user"""
    user = update.message.from_user
    userID = user.id
    S3_key = database.pictures.getLastPictureS3KeybyUserID(userID)

    # Photo will be downloaded on server in this temp directory before sending to user
    picturePath = publ.photoFolderPath + TIME + ".jpg"
    bot.send_message(chat_id=update.message.chat_id,
                     text="Подождите, идет загрузка")
    bot.send_chat_action(chat_id=update.message.chat_id,
                         action=ChatAction.TYPING)
    S3Instance().s3client.download_file(publ.s3_picturesbucket, S3_key, picturePath)
    bot.send_photo(chat_id=update.message.chat_id,
                   photo=open(picturePath, 'rb'))
    rm(publ.photoFolderPath + "*") # Delete photo from temporary directory


def getAllMyPictures(bot, update):
    """Retrieve all photos from database belonging to user and send it back to user"""
    user = update.message.from_user
    userID = user.id

    picturesKeyList = database.pictures.getListOfUserS3Keys(userID)

    for pictureKey in picturesKeyList:
        picturePath = publ.photoFolderPath + pictureKey + ".jpg"
        S3Instance().s3client.download_file(publ.s3_picturesbucket, pictureKey, picturePath)
        bot.send_photo(chat_id=update.message.chat_id,
                       photo=open(picturePath, 'rb'))

    bot.send_message(chat_id=update.message.chat_id,
                     text="Все картинки отправлены")

    rm(publ.photoFolderPath + "*")  # Delete photos from temporary directory


def updateName(bot, update, args):
    """Set Name to the picture"""

    user = update.message.from_user
    userID = user.id

    ID = str(args[0])
    Name = str(args[1])

    if pictureExists(ID):
        if hasAccess(userID, ID):
            database.pictures.definePictureName(ID, Name)
            bot.send_message(chat_id=update.message.chat_id, text="Имя картинки с ID {} успешно сменено на {}".format(ID, Name))
        else:
            bot.send_message(chat_id=update.message.chat_id,
                             text="Извините, вы не являетесь владельцем картинки {}".format(ID))
    else:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Извините, картинки {} не существует".format(ID))


def getPictyreByID(bot, update, args):
    """Sends picture with ID = ID to user"""

    user = update.message.from_user
    userID = user.id

    ID = str(args[0])

    if pictureExists(ID):
        if hasAccess(userID, ID) or isPublic(ID):
            S3_key = database.pictures.getS3KeybyID(ID)

            picturePath = publ.photoFolderPath + TIME + ".jpg"
            bot.send_message(chat_id=update.message.chat_id, text="Подождите, идет загрузка")
            S3Instance().s3client.download_file(publ.s3_picturesbucket, S3_key, picturePath)
            bot.send_photo(chat_id=update.message.chat_id,
                           photo=open(picturePath, 'rb'))
            rm(publ.photoFolderPath + "*")
        else:
            bot.send_message(chat_id=update.message.chat_id,
                             text="Извините, картинка {} приватная".format(ID))
    else:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Извините, картинки {} не существует".format(ID))


def deletePictureByID(bot, update, args):
    """Deletes picture with given ID from DB"""
    user = update.message.from_user
    userID = user.id

    ID = str(args[0])

    if pictureExists(ID):
        if hasAccess(userID, ID):
            S3_key = database.pictures.getS3KeybyID(ID)
            S3Instance().s3client.delete_object(Bucket=publ.s3_picturesbucket, Key=S3_key)
            database.pictures.deletePictureByID(ID)
            bot.send_message(chat_id=update.message.chat_id, text="Картинка успешно удалена")
        else:
            bot.send_message(chat_id=update.message.chat_id, text="Только владелец картинки может удалить ее")
    else:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Извините, картинки {} не существует".format(ID))


def setPublic(bot, update, args):
    """Set picture privacy policy to public"""
    user = update.message.from_user
    userID = user.id

    ID = str(args[0])

    if pictureExists(ID):
        if hasAccess(userID, ID):
            database.pictures.setPublic(ID)
            bot.send_message(chat_id=update.message.chat_id,
                             text="Картинка теперь публичная")
        else:
            bot.send_message(chat_id=update.message.chat_id,
                             text="Только владелец картинки может сделать ее публичной")
    else:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Извините, картинки {} не существует".format(ID))



def getUserPictures(bot, update):
    """Return user picture IDs separated by comma"""
    user = update.message.from_user
    userID = user.id

    res = database.pictures.getStringOfUserPictures(userID)

    bot.send_message(chat_id=update.message.chat_id,
                     text=res)


def getOwnerOfPicture(bot, update, args):
    """Return owner of the picture"""
    pictureID = args[0]
    owner = database.pictures.getOwnerNamebyPictureID(pictureID)
    bot.send_message(chat_id=update.message.chat_id,
                     text=owner)


# TODO Функция которая возвращает пользовтелю список его картинок вида Картинка1, Картника2 и 4 картинки без имени
# TODO Функция присылания случайной публичной картинки
# TODO Разнести фцнкции в подпапку по категориям