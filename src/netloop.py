
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
    while True:
        try:
            now = datetime.now().time()
            if time(7) <= now <= time(16, 59):
                act.set_net_control("/net 100 600", ["isi", "i-"])
            if time(17) <= now <= time(20, 59):
                act.set_net_control("/net 50 400", ["isi", "i-"])
            elif time(21) <= now <= time(23, 59):
                act.set_net_control("/net 20 100", ["isi", "i-"])
            while time(0) <= now <= time(6, 59):
                act.ofuscate("/ofuscate isi 10 10")
                sleep(uniform(5.0, 20.0))
            sleep(15*60)
        except (AssertionError, req_exceptions.ConnectTimeout, req_exceptions.ConnectionError, req_exceptions.HTTPError, req_exceptions.ReadTimeout, req_exceptions.Timeout) as e:
            logger.warning(e, exc_info=True)
            sleep(uniform(1.0, 2.0))
        except Exception:
            logger.exception("Exception occurred")
            sleep(uniform(1.0, 2.0))
