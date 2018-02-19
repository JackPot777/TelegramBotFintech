"""
Inside this file logging function will be located
"""

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def error(bot, update, error):
    """Log errors caused by updates"""
    logger.warning('Update "%s" caused error "%s"', update, error)