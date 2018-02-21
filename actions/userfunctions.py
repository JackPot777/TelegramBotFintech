# -*- coding: utf-8 -*-
"""
File with functions that can be called by any user
To call a function user should type /<function> in chat window

Don't Forget to add function to Command Handler!

"""
from configuration.private import PASSWORD_LIST, SECRET_CHANNEL_LINK
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def start(bot, update):
    """Send greetings message"""
    bot.send_message(chat_id=update.message.chat_id,
                     text="Вечер в хату господа")


def getMyUserName(bot, update):
    """Send Username back"""
    user = update.message.from_user
    bot.send_message(chat_id=update.message.chat_id,
                     text=user['username'])


def getMyId(bot, update):
    """Send User Id back"""
    user = update.message.from_user
    bot.send_message(chat_id=update.message.chat_id,
                     text=user['id'])


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
    userPassword = " ".join(args)
    if userPassword in PASSWORD_LIST:
        keyboard = [[InlineKeyboardButton(text="Link to Secret channel", url=SECRET_CHANNEL_LINK)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(text="Click to join:",reply_markup=reply_markup)
    else:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Wrong password")


def getLinkButton(bot, update):
    """Message with button with url leading to secret channel"""
    query = update.callback_query
    bot.edit_message_text(text="Button",
                          chat_id=query.message.chat_id,
                          parse_mode= "HTML",
                          message_id=query.message.message_id)