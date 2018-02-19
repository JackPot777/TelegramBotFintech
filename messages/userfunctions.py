# -*- coding: utf-8 -*-
"""
Inside this file functions, that can be called by user are located.
To call a function user should type /<function> in chat window

Don't Forget to add function to Command Handler!

"""

def start(bot, update):
    """Send greetings message"""
    bot.send_message(chat_id=update.message.chat_id,
                     text="Вечер в хату господа")



def getAdmins(bot, update):
    """Get list of Administrators"""
    bot.get_chat_administrators(chat_id=update.message.chat_id)



def getAnswer(bot, update):
    """Send Answer to the Ultimate Question of Life, the Universe, and Everything"""
    bot.send_message(chat_id=update.message.chat_id,
                     text=42)


def getC3PO(bot, update):
    """Send C-3PO pic to chat"""
    bot.send_photo(chat_id=update.message.chat_id,
                   photo="https://lumiere-a.akamaihd.net/v1/images/C-3PO-See-Threepio_68fe125c.jpeg?region=0%2C1%2C1408%2C792&width=768")