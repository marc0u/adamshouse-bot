
import logging
from marcotools import telegrambot
from marcotools import filestools
import src.actions as act

HELP_MSG = """/camstart : Start all cameras.
/camstatus : Get status for each cameras.
/startvport : Start a vport for a while. Ex. /startvport IP InPort OutPort AliveMin
/torrent : Start torrent for a while. Ex. /torrent AliveMin
/proxmox : Start proxmox for a while. Ex. /proxmox AliveMin
/net0 : Set net control normal mode
/net1 : Set net control moderate mode
/net2 : Set net control restrictive mode
/net3 : Set net control very restrict mode"""

tb = telegrambot.tb('921941981:AAHzGw2Nx3BXD4hDoYsfWqZOAlcP2a6zxqI')
tg_users = filestools.load_json_file("./src/users.json")


def resp_handler(update_info):
    text, chat, user = update_info

    def admin(user_name):
        if text.lower() == '/help':
            tb.send_message(HELP_MSG, chat)
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
