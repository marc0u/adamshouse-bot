import logging
from datetime import datetime
from time import sleep
import os.path
import random

from marcotools import schedule
from marcotools import filestools
from marcotools import logtools as lt
from marcotools import telegrambot as tgbot
from requests import exceptions as req_exceptions
from src.resphandler import resp_handler
import src.actions as act

tb = tgbot.tb('921941981:AAHzGw2Nx3BXD4hDoYsfWqZOAlcP2a6zxqI')
filename = os.path.basename(__file__)
# lt.log_start(filename)
logging.basicConfig(format='%(asctime)s - %(levelname)s / %(module)s / %(funcName)s / %(message)s',
                    datefmt='%H:%M:%S', level=logging.ERROR)

tg_users = filestools.load_json_file("./src/users.json")

# Schedule
schedule.every().day.at("07:00").do(act.netcontrol, 50, 300)
schedule.every().day.at("21:00").do(act.netcontrol, 50, 150)
schedule.every().day.at("22:00").do(act.netcontrol, 50, 100)
schedule.every().day.at("23:00").do(act.netcontrol, 50, 50)
schedule.every().day.at("00:00").do(act.netcontrol, 50, 25)

# Main
tb.send_message('AdamHouse started at ' +
                datetime.now().strftime("%H:%M:%S"), tg_users['marco']['id'])
while True:
    try:
        tb.updates_handler(resp_handler)
        schedule.run_pending()
        sleep(1.0)
    except (AssertionError, req_exceptions.ConnectTimeout, req_exceptions.ConnectionError, req_exceptions.HTTPError, req_exceptions.ReadTimeout, req_exceptions.Timeout) as e:
        logging.warning(e)
        sleep(random.uniform(1.0, 2.0))
    except Exception:
        logging.exception("Exception occurred")
        sleep(random.uniform(1.0, 2.0))
    except KeyboardInterrupt:
        break

tb.send_message('AdamHouse manually closed at ' +
                datetime.now().strftime("%H:%M:%S"), tg_users['marco']['id'])
