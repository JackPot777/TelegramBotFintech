"""
File with functions, that can be used only by admins
"""

from configuration.private import ADMIN_PASSWORD, ADMINS_LIST
from configuration.public import admin_auto_login
# List storing currently logged in Admins
loginedAdmins = []

if admin_auto_login == True:
    loginedAdmins.extend(ADMINS_LIST)

adminListString = "\n".join(map(str, loginedAdmins))


def login(bot, update, args):
    """Command for admin authorization"""
    userID = update.message.from_user['id']
    userPassword = " ".join(args)
    if userPassword == ADMIN_PASSWORD and userID not in loginedAdmins:
        loginedAdmins.append(userID)
        bot.send_message(chat_id=update.message.chat_id,
                         text="Successful Login, greetings " + str(userID))
    elif userPassword == ADMIN_PASSWORD and userID in loginedAdmins:
        bot.send_message(chat_id=update.message.chat_id,
                         text="You are already logged in")
    else:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Get out of here, Stalker")


def logout(bot, update):
    """Command for admin logout"""
    userID = update.message.from_user['id']
    if userID in loginedAdmins:
        loginedAdmins.remove(userID)
        bot.send_message(chat_id=update.message.chat_id,
                         text="Successful Logout, bye bye")
    else:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Log in before log out")


def loginStatus(bot, update):
    """Check whether admin is logged in"""
    userID = update.message.from_user['id']
    if userID in loginedAdmins:
        bot.send_message(chat_id=update.message.chat_id,
                         text="You are currently logged in")
    else:
        bot.send_message(chat_id=update.message.chat_id,
                         text="You are not logged in")


def getLoggedInAdmins(bot, update):
    """Prints admin that are currently logged in"""
    userID = update.message.from_user['id']
    if userID in loginedAdmins:
        bot.send_message(chat_id=update.message.chat_id,
                         text=adminListString)
    else:
        bot.send_message(chat_id=update.message.chat_id,
                         text="You are not logged in")