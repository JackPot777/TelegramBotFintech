"""
Inside this file functions, working with text are located
"""

def echo(bot, update):
    """Upon receiving message, sends it back"""
    bot.send_message(chat_id=update.message.chat_id,
                     text=update.message.text)
