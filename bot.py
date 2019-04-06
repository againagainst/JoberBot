#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import configparser

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import gen

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text("Someone want to do a job")


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        """Here is the list of my commands:

/job — to get a job
/advice — to get HR advice

I may send a piece of advice when needed.
"""
    )


def job(bot, update):
    txt = gen.jobmaker.make_jobline()
    logging.info("Generated job: %s", txt)
    update.message.reply_text(txt)


def advice(bot, update):
    txt = gen.jobmaker.make_response()
    logging.info("Generated advice: %s", txt)
    update.message.reply_text(txt)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    config = configparser.ConfigParser()
    config.read("config.ini")
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token=config["telegram"]["token"])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("job", job))
    dp.add_handler(CommandHandler("advice", advice))
    dp.add_handler(CommandHandler("help", help))
    # dp.

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
