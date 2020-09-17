import logging
from datetime import datetime
from time import sleep
import os.path
import random

from marcotools import schedule
from marcotools import logtools as lt
from marcotools import telegrambot as tgbot
from requests import exceptions as req_exceptions

import src.actions as act

tb = tgbot.tb('921941981:AAHzGw2Nx3BXD4hDoYsfWqZOAlcP2a6zxqI')
filename = os.path.basename(__file__)
# lt.log_start(filename)
logging.basicConfig(format='%(asctime)s - %(levelname)s / %(module)s / %(funcName)s / %(message)s',
                    datefmt='%H:%M:%S', level=logging.E)

tg_users = {
    'marco': {
        'id': 165270556,
        'name': 'Marco',
    },
    'aiara': {
        'id': 167143888,
        'name': 'Aiara'
    },
    'quelo': {
        'id': 618984973,
        'name': 'Exequiel'
    }
}

# Schedule
schedule.every().day.at("07:00").do(act.netcontrol, 50, 300)
schedule.every().day.at("21:00").do(act.netcontrol, 50, 150)
schedule.every().day.at("22:00").do(act.netcontrol, 50, 100)
schedule.every().day.at("23:00").do(act.netcontrol, 50, 50)
schedule.every().day.at("00:00").do(act.netcontrol, 50, 25)


def resp_handler(update_info):
    text, chat, user = update_info

    def admin(user_name):
        if text.lower() == '/help':
            msg = """/camstart : Start all cameras.
/camstatus : Get status for each cameras.
/startvport : Start a vport for a while. Ex. /startvport IP InPort OutPort AliveMin
/torrent : Start torrent for a while. Ex. /torrent AliveMin
/proxmox : Start proxmox for a while. Ex. /proxmox AliveMin
/net0 : Set net control normal mode
/net1 : Set net control moderate mode
/net2 : Set net control restrictive mode
/net3 : Set net control very restrict mode"""
            tb.send_message(msg, chat)
        elif text.lower() == '/camstart':
            act.camstart(tb, chat, user_name)
        elif text.lower() == '/camstatus':
            act.camstatus(tb, chat)
        elif '/startvport' in text.lower():
            act.startvport(tb, chat, text.lower())
        elif '/torrent' in text.lower():
            act.start_torrent(tb, chat, text.lower())
        elif '/proxmox' in text.lower():
            act.proxmox(tb, chat, text.lower())
        elif text.lower() == '/net0':
            act.netcontrol(50, 300, tb, chat)
        elif text.lower() == '/net1':
            act.netcontrol(20, 150, tb, chat)
        elif text.lower() == '/net2':
            act.netcontrol(10, 50, tb, chat)
        elif text.lower() == '/net3':
            act.netcontrol(5, 25, tb, chat)
        else:
            tb.send_message('Wrong command!', chat)

    def users(user_name):
        if text.lower() == 'cams':
            act.camstart(tb, chat, user_name, tg_users['marco']['id'])
        else:
            tb.send_message(
                f'Envía la palabra "Cams" para habilitar las camaras"', chat)

    if user == tg_users['marco']['id']:
        admin(tg_users['marco']['name'])
    elif user == tg_users['aiara']['id']:
        users(tg_users['aiara']['name'])
    elif user == tg_users['quelo']['id']:
        users(tg_users['quelo']['name'])
    else:
        logging.warning('Someone strange is trying to connect with the bot.')
        tb.send_message(
            'WARNING: Someone strange is trying to connect with the bot.', tg_users['marco']['id'])
        tb.send_message('Username wrong!', chat)


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
