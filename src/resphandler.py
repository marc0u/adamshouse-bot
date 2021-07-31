
import logging
import telegram
from os import getenv
from marcotools import telegrambot
from marcotools import filestools
import src.actions as act


HELP_MSG = """/time : Get server time.
/startcams alive_min:0-9999
/camstatus : Get status for each cameras.
/startvport ip:1-254 inPort:0-65535 outPort:0-65535 aliveMin:1-9999
/net up_limit:1-9999 down_limit:0-9999
/addvport ip:1-254 inPort:0-65535 outPort:0-65535
/removevport ip:1-254 inPort:0-65535 outPort:0-65535
/ofuscate someone how_many:1-9999" interval_sec:1-9999
/reboot : Reboot router
"""

# tb = telegrambot.tb(getenv("TB_TOKEN"))
tb = telegram.Bot(token=getenv("TB_TOKEN"))
tg_users = filestools.load_json_file("./src/users.json")
settings = filestools.load_json_file("./src/settings.json")


def resp_handler(update_info):
    text, chat, user = update_info
    # text = text.lower()

    if user == tg_users['marco']['id']:
        admin(tg_users['marco']['name'], text, chat)
    elif user == tg_users['aiara']['id']:
        users(tg_users['aiara']['name'], text, chat)
    elif user == tg_users['quelo']['id']:
        users(tg_users['quelo']['name'], text, chat)
    else:
        logging.warning('Someone strange is trying to connect with the bot.')
        tb.send_message(text='WARNING: Someone strange is trying to connect with the bot.',
                        chat_id=tg_users['marco']['id'])
        tb.send_message(text='Username wrong!', chat_id=chat)


def admin(user_name, text, chat):
    if text.startswith('/help'):
        return tb.send_message(text=HELP_MSG, chat_id=chat)
    elif text.startswith('/startcams'):
        return act.start_cams(tb, chat, user_name, text)
    elif text.startswith('/camstatus'):
        return act.are_cams_alive(tb, chat)
    elif text.startswith('/startvport'):
        return act.start_vport(tb, chat, text)
    elif text.startswith('/net'):
        return act.set_net_control(text, tb, chat)
    elif text.startswith('/addvport'):
        return act.add_vport(tb, chat, text)
    elif text.startswith('/removevport'):
        return act.remove_vport(tb, chat, text)
    elif text.startswith('/ofuscate'):
        return act.ofuscate(text, tb, chat)
    elif text.startswith('/reboot'):
        act.tenda.reboot()
        return tb.send_message(text="Router rebooted", chat_id=chat)
    elif text.startswith('/time'):
        return act.get_time(tb, chat)
    elif text.startswith('/ip'):
        return act.get_public_ip(tb, chat)
    else:
        return tb.send_message(text='Wrong command!', chat_id=chat)


def users(user_name, text, chat):
    if text == 'cams':
        act.start_cams(tb, chat, user_name, "/startcams 10",
                       tg_users['marco']['id'])
    else:
        tb.send_message(
            text=f'Envía la palabra "Cams" para habilitar las camaras"', chat_id=chat)
