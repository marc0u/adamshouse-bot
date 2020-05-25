import logging
from datetime import datetime
from time import sleep
import os.path

import src.schedule

import src.logtools as lt
import src.nettools as nt
import src.telegrambot as tgbot
import src.actions as act

tb = tgbot.tb('921941981:AAHzGw2Nx3BXD4hDoYsfWqZOAlcP2a6zxqI')
filename = os.path.basename(__file__)
# lt.log_start(filename)
logging.basicConfig(format='%(asctime)s - %(levelname)s / %(module)s / %(funcName)s / %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

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

## Schedule
## Monday
src.schedule.every().monday.at("07:00").do(act.netcontrol, 50, 300)
src.schedule.every().monday.at("21:00").do(act.netcontrol, 50, 150)
src.schedule.every().monday.at("22:00").do(act.netcontrol, 50, 100)
src.schedule.every().monday.at("23:00").do(act.netcontrol, 50, 50)
src.schedule.every().monday.at("00:00").do(act.netcontrol, 50, 25)
## Tuesday
src.schedule.every().tuesday.at("07:00").do(act.netcontrol, 50, 300)
src.schedule.every().tuesday.at("21:00").do(act.netcontrol, 50, 150)
src.schedule.every().tuesday.at("22:00").do(act.netcontrol, 50, 100)
src.schedule.every().tuesday.at("23:00").do(act.netcontrol, 50, 50)
src.schedule.every().tuesday.at("00:00").do(act.netcontrol, 50, 25)
## Wednesday
src.schedule.every().wednesday.at("07:00").do(act.netcontrol, 50, 300)
src.schedule.every().wednesday.at("21:00").do(act.netcontrol, 50, 150)
src.schedule.every().wednesday.at("22:00").do(act.netcontrol, 50, 100)
src.schedule.every().wednesday.at("23:00").do(act.netcontrol, 50, 50)
src.schedule.every().wednesday.at("00:00").do(act.netcontrol, 50, 25)
## Thursday
src.schedule.every().thursday.at("07:00").do(act.netcontrol, 50, 300)
src.schedule.every().thursday.at("21:00").do(act.netcontrol, 50, 150)
src.schedule.every().thursday.at("22:00").do(act.netcontrol, 50, 100)
src.schedule.every().thursday.at("23:00").do(act.netcontrol, 50, 50)
src.schedule.every().thursday.at("00:00").do(act.netcontrol, 50, 25)
## Friday
src.schedule.every().friday.at("07:00").do(act.netcontrol, 50, 300)
src.schedule.every().friday.at("21:00").do(act.netcontrol, 50, 150)
src.schedule.every().friday.at("23:00").do(act.netcontrol, 50, 100)
src.schedule.every().friday.at("00:00").do(act.netcontrol, 50, 50)
src.schedule.every().friday.at("00:45").do(act.netcontrol, 50, 25)
## Saturday
src.schedule.every().saturday.at("07:00").do(act.netcontrol, 50, 300)
src.schedule.every().saturday.at("21:00").do(act.netcontrol, 50, 150)
src.schedule.every().saturday.at("23:00").do(act.netcontrol, 50, 100)
src.schedule.every().saturday.at("00:00").do(act.netcontrol, 50, 50)
src.schedule.every().saturday.at("00:45").do(act.netcontrol, 50, 25)
## Sunday
src.schedule.every().sunday.at("07:00").do(act.netcontrol, 50, 300)
src.schedule.every().sunday.at("21:00").do(act.netcontrol, 50, 150)
src.schedule.every().sunday.at("22:00").do(act.netcontrol, 50, 100)
src.schedule.every().sunday.at("23:00").do(act.netcontrol, 50, 50)
src.schedule.every().sunday.at("00:00").do(act.netcontrol, 50, 25)

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
            tb.send_message(f'Envía la palabra "Cams" para habilitar las camaras"', chat)

    if user == tg_users['marco']['id']:
        admin(tg_users['marco']['name'])
    elif user == tg_users['aiara']['id']: 
        users(tg_users['aiara']['name'])
    elif user == tg_users['quelo']['id']:
        users(tg_users['quelo']['name'])
    else:
        logging.warning('Someone strange is trying to connect with the bot.')
        tb.send_message('WARNING: Someone strange is trying to connect with the bot.', tg_users['marco']['id'])
        tb.send_message('Username wrong!', chat)

## Main
logging.info('AdamsHouse started!')
tb.send_message('AdamHouse started at ' + datetime.now().strftime("%H:%M:%S"), tg_users['marco']['id'])
while True:
    try:
        tb.bot_Handler(resp_handler)
        src.schedule.run_pending()
        sleep(1.0)
    except Exception:
        logging.exception("Exception occurred")
        sleep(5.0)