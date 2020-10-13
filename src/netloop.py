
import logging
from random import uniform
from datetime import datetime, time
from time import sleep
from requests import exceptions as req_exceptions
from marcotools import filestools
import src.actions as act

# settings = filestools.load_json_file("./src/settings.json")


def NetControl():
    while True:
        try:
            now = datetime.now().time()
            if time(7) <= now <= time(20, 59):
                act.set_net_control("/net 50 400", ["isi", "i-"])
            elif time(21) <= now <= time(23, 30):
                act.set_net_control("/net 20 100", ["isi", "i-"])
            elif time(23, 31) <= now <= time(6, 59):
                act.set_net_control("/net 20 50", ["isi", "i-"])
                act.ofuscate("/ofuscate isi 10 5")
            sleep(15*60)
        except (AssertionError, req_exceptions.ConnectTimeout, req_exceptions.ConnectionError, req_exceptions.HTTPError, req_exceptions.ReadTimeout, req_exceptions.Timeout) as e:
            logging.warning(e)
            sleep(uniform(1.0, 2.0))
        except Exception:
            logging.exception("Exception occurred")
            sleep(uniform(1.0, 2.0))
