
import logging
from marcotools import telegrambot
from marcotools import filestools
import src.actions as act

HELP_MSG = """/startcams alive_min:0-9999
/camstatus : Get status for each cameras.
/startvport ip:1-254 inPort:0-65535 outPort:0-65535 aliveMin:1-9999
/net up_limit:1-9999 down_limit:0-9999
/addvport ip:1-254 inPort:0-65535 outPort:0-65535
/removevport ip:1-254 inPort:0-65535 outPort:0-65535
/ofuscate someone how_many:1-9999" interval_sec:1-9999
/reboot : Reboot router
"""

tb = telegrambot.tb('921941981:AAHzGw2Nx3BXD4hDoYsfWqZOAlcP2a6zxqI')
tg_users = filestools.load_json_file("./src/users.json")
settings = filestools.load_json_file("./src/settings.json")


def resp_handler(update_info):
    text, chat, user = update_info
    text = text.lower()

    def admin(user_name):
        if text.startswith('/help'):
            tb.send_message(HELP_MSG, chat)
        elif text.startswith('/startcams'):
            act.start_cams(tb, chat, user_name, text)
        elif text.startswith('/camstatus'):
            act.are_cams_alive(tb, chat)
        elif text.startswith('/startvport'):
            act.start_vport(tb, chat, text)
        elif text.startswith('/net'):
            act.set_net_control(text, settings["blacklist"], tb, chat)
        elif text.startswith('/addvport'):
            act.add_vport(tb, chat, text)
        elif text.startswith('/removevport'):
            act.remove_vport(tb, chat, text)
        elif text.startswith('/ofuscate'):
            act.ofuscate(text, tb, chat)
        elif text.startswith('/reboot'):
            act.tenda.reboot()
            tb.send_message("Router rebooted", chat)
        else:
            tb.send_message('Wrong command!', chat)

    def users(user_name):
        if text == 'cams':
            act.start_cams(tb, chat, user_name, "/startcams 10",
                           tg_users['marco']['id'])
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
