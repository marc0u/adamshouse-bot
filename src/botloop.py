import logging
from datetime import datetime
from random import uniform
from time import sleep
from requests import exceptions as req_exceptions
import src.resphandler as rh

logger = logging.getLogger("adamshouse.botloop")

def Bot():
    rh.tb.send_message('AdamHouse started at ' +
                       datetime.now().strftime("%H:%M:%S"),  rh.tg_users['marco']['id'])
    while True:
        try:
            rh.tb.updates_handler(rh.resp_handler)
            sleep(1.0)
        except (AssertionError, req_exceptions.ConnectTimeout, req_exceptions.ConnectionError, req_exceptions.HTTPError, req_exceptions.ReadTimeout, req_exceptions.Timeout) as e:
            logger.warning(e, exc_info=True)
            sleep(uniform(1.0, 2.0))
        except Exception:
            logger.exception("Exception occurred")
            sleep(uniform(1.0, 2.0))
