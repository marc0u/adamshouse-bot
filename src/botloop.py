import logging
from datetime import datetime
from time import sleep
from os import getenv
import src.resphandler as rh
from marcotools import telegrambot

logger = logging.getLogger("adamshousebot.botloop")

tb = telegrambot.tb(getenv("TB_TOKEN"))


def Bot():
    started = datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' AdamshouseBot started'
    print(started)
    tb.send_message(started,  getenv("LOGGER_TB_CHAT_ID"))
    logger.debug("--------DEBUG MODE-------")
    error_counter = 0
    while True:
        try:
            tb.updates_handler(rh.resp_handler)
            sleep(3.0)
        except Exception as err:
            if error_counter > 3:
                continue
            logger.exception("Exception occurred")
            tb.send_message(err,  getenv("LOGGER_TB_CHAT_ID"))
            sleep(3.0)
