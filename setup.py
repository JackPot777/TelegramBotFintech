from distutils.core import setup

with open('README.MD') as file:
    long_descrition = file.read()

setup(name='TelegramBotFintech',
      version='0.2.1',
      description='Telegram bot for university project',
      url='https://github.com/Saymjn/TelegramBotFintech',
      long_description=long_descrition,
      install_requires=['python-telegram-bot']
)