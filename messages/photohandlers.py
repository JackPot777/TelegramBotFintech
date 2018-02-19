# -*- coding: utf-8 -*-
"""
Inside this file functions, working with photos are located
"""
from time import gmtime, strftime

TIME = strftime("%Y_%m_%d_%H_%M_%S", gmtime())

def downloadPhoto(bot, update):
    """Download photo sent by user"""
    file_id = update.message.photo[-1].file_id
    newFile = bot.getFile(file_id)
    newFile.download('data/downloadedPhotos/photo_' + TIME + '.jpg')
    bot.send_message(chat_id=update.message.chat_id,
                     text="Картинка успешно скачана")