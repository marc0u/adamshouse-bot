import logging
from datetime import datetime
from random import uniform
from time import sleep
from requests import exceptions as req_exceptions
import src.resphandler as rh


def Bot():
    rh.tb.send_message('AdamHouse started at ' +
                       datetime.now().strftime("%H:%M:%S"),  rh.tg_users['marco']['id'])
    while True:
        try:
            rh.tb.updates_handler(rh.resp_handler)
            sleep(1.0)
        except (AssertionError, req_exceptions.ConnectTimeout, req_exceptions.ConnectionError, req_exceptions.HTTPError, req_exceptions.ReadTimeout, req_exceptions.Timeout) as e:
            logging.warning(e)
            sleep(uniform(1.0, 2.0))
        except Exception:
            logging.exception("Exception occurred")
            sleep(uniform(1.0, 2.0))
