# -*- coding: utf-8 -*-
"""
File with handlers involving photos
"""


import configuration.public as publ
import database.pictures
from utils.S3 import S3Instance
from time import gmtime, strftime
from utils.misc import rm


def downloadPhoto(bot, update):
    """Download photo sent by user"""

    user = update.message.from_user
    userID = str(user.id) # If not converted into string causes TypeError
    userName = user.first_name

    TIME = strftime("%Y_%m_%d_%H_%M_%S", gmtime())

    file_id = update.message.photo[-1].file_id
    newFile = bot.getFile(file_id)

    KEY = "photo_" + userID + "_" + TIME + ".jpg"
    filePath = publ.photoFolderPath + KEY

    newFile.download(filePath)

    S3Instance().s3client.upload_file(filePath, publ.s3_picturesbucket, KEY) # Save picture to S3
    database.pictures.insertIntoPictures(userID=userID, UserName=userName, S3_Key=KEY) # Insert Key in Database
    rm(publ.photoFolderPath + "*") # Delete picture from server

    ID = database.pictures.getIDbyS3Key(KEY)

    bot.send_message(chat_id=update.message.chat_id, text="Картинка успешно загружена, её ID = " + ID)