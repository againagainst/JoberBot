#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import configparser
import random

from telegram import MessageEntity, Chat
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


def bot_help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        """Вот что я могу:

Комманда /job — выдам профессию из "Единого тарифно-квалификационного справочника работ и профессий рабочих".

Могу помогать советами по найму в ответах на случайные реплики.
Обязан дать совет по найму при прямом упоминании в группе и всегда в личных сообщениях.
"""
    )


def job(bot, update):
    txt = gen.jobmaker.make_jobline()
    logging.info("Generated job: %s", txt)
    update.message.reply_text(txt)


def advice(bot, update):
    txt = gen.jobmaker.make_response()
    logging.info("Generated advice: %s", txt)
    update.message.reply_text(txt, quote=True)


def recommendation(bot, update):
    is_private = update.effective_chat.type == Chat.PRIVATE
    if not is_private:
        if update.message.text:
            probability = bot.probability + len(str(len(update.message.text)))
            if random.randint(0, 100) < probability:
                logging.info(
                    "Random event with probability %d percent", probability
                )
            else:
                return
        else:
            return

    advice(bot, update)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def get_probability_from_config(config):
    try:
        return int(config["telegram"]["probability"])
    except KeyError:
        return 0


def main():
    """Start the bot."""
    config = configparser.ConfigParser()
    config.read("config.ini")
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token=config["telegram"]["token"])

    # Proxy Version
    # REQUEST_KWARGS = {"proxy_url": "socks5h://127.0.0.1:9150"}
    # updater = Updater(token=config["telegram"]["token"], request_kwargs=REQUEST_KWARGS)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    updater.bot.probability = get_probability_from_config(config)

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", callback=start))
    dp.add_handler(CommandHandler("job", callback=job))
    dp.add_handler(CommandHandler("help", callback=bot_help))
    mention_handler = MessageHandler(
        Filters.text
        & Filters.entity(MessageEntity.MENTION)
        & Filters.regex("@huntflow_jober_bot"),
        callback=advice,
    )
    dp.add_handler(mention_handler)
    recommendation_handler = MessageHandler(filters=None, callback=recommendation)
    dp.add_handler(recommendation_handler)
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
