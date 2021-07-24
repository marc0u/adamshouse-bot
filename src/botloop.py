import logging
from datetime import datetime
from random import uniform
from time import sleep
from os import getenv
from requests import exceptions as req_exceptions
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
    warn_counter = 0
    while True:
        try:
            tb.updates_handler(rh.resp_handler)
            error_counter = 0
            warn_counter = 0
            sleep(3.0)
        except (AssertionError, req_exceptions.ConnectTimeout, req_exceptions.ConnectionError, req_exceptions.HTTPError, req_exceptions.ReadTimeout, req_exceptions.Timeout) as e:
            warn_counter += 1
            if warn_counter > 3:
                logger.exception("Exception occurred")
                sleep(15*60)
            logger.warning(e, exc_info=True)
            sleep(3.0)
        except Exception:
            error_counter += 1
            if error_counter > 1:
                logger.exception("Exception occurred")
                sleep(15*60)
            sleep(5.0)
