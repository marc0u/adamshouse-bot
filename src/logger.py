import logging
from os import getenv
from marcotools import telegrambot
from logging import Handler
from logging.handlers import RotatingFileHandler


class TelegramBotHandler(Handler):
    _TB = telegrambot.tb(getenv("LOGGER_TB_TOKEN"))

    def send_message(self, msg):
        try:
            return self._TB.send_message(msg,
                                         getenv("LOGGER_TB_CHAT_ID"))
        except:
            return

    def emit(self, record):
        log = self.format(record)
        return self.send_message(log[:1000])


def init_logger(name, debug=""):
    # Main logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # Logging Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(funcName)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    formatter_short = logging.Formatter(
        '%(name)s - %(funcName)s - %(levelname)s: %(message)s')
    if debug == "true":
        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    else:
        # File Handler
        file_handler = RotatingFileHandler(f'{name}.log', mode='a', maxBytes=2*1024*1024,
                                           backupCount=2, encoding=None, delay=0)
        file_handler.setLevel(logging.ERROR)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        # # TelegramBot Handler
        # tb_handler = TelegramBotHandler()
        # tb_handler.setLevel(logging.ERROR)
        # tb_handler.setFormatter(formatter_short)
        # logger.addHandler(tb_handler)
    return logger
