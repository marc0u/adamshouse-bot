
import logging
from random import uniform
from datetime import datetime, time
from time import sleep
from requests import exceptions as req_exceptions
from marcotools import filestools
import src.actions as act

# settings = filestools.load_json_file("./src/settings.json")

logger = logging.getLogger("adamshouse.netloop")


def NetControl():
    error_counter = 0
    warn_counter = 0
    while True:
        try:
            now = datetime.now().time()
            if time(7) <= now <= time(20, 59):
                act.set_net_control("/net 100 600 100-199")
            elif time(21) <= now <= time(22, 59):
                act.set_net_control("/net 50 300 100-199")
            elif time(23) <= now <= time(23, 59):
                act.set_net_control("/net 50 150 100-199")
                act.ofuscate("/ofuscate 10 10 100-199")
            elif time(0) <= now <= time(0, 59):
                act.set_net_control("/net 20 50 100-199")
                act.ofuscate("/ofuscate 10 10 100-199")
            elif time(1) <= now <= time(6, 59):
                act.set_net_control("/net 10 30 100-199")
                act.ofuscate("/ofuscate 10 10 100-199")
            error_counter = 0
            warn_counter = 0
            sleep(uniform(5.0, 10.0)*60)
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
