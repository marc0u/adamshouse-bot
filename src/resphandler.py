
import logging
import telegram
from os import getenv
from marcotools import telegrambot
from marcotools import filestools
import src.actions as act

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
        return act.help(tb, chat)
    elif text.startswith('/startcams'):
        return act.start_cams(tb, chat, user_name, text)
    elif text.startswith('/camstatus'):
        return act.are_cams_alive(tb, chat)
    elif text.startswith('/startvport'):
        return act.start_vport(tb, chat, text)
    elif text.startswith('/netcontrol'):
        return act.get_net_control(tb, chat)
    elif text.startswith('/net'):
        return act.set_net_control(tb, chat, text)
    elif text.startswith('/addvport'):
        return act.add_vport(tb, chat, text)
    elif text.startswith('/removevport'):
        return act.remove_vport(tb, chat, text)
    elif text.startswith('/ofuscate'):
        return act.ofuscate(tb, chat, text)
    elif text.startswith('/reboot'):
        act.tenda.reboot()
        return tb.send_message(text="Router rebooted", chat_id=chat)
    elif text.startswith('/time'):
        return act.get_time(tb, chat)
    elif text.startswith('/ip'):
        return act.get_public_ip(tb, chat)
    elif text.startswith('/backup'):
        return act.backup_ipmac_bind(tb, chat)
    elif text.startswith('/restore'):
        return act.restore_ipmac_bind(tb, chat)
    elif text.startswith('/online'):
        return act.get_online_clients(tb, chat)
    elif text.startswith('/setuprouter'):
        return act.setup_router(tb, chat)
    elif text.startswith('/setuprouter2'):
        return act.setup_router2(tb, chat)
    else:
        return tb.send_message(text='Wrong command!', chat_id=chat)


def users(user_name, text, chat):
    if 'cams' in text.lower():
        act.start_cams(tb, chat, user_name, "/startcams 10",
                       tg_users['marco']['id'])
    elif 'wifi' in text.lower():
        return act.setup_router(tb, chat)
    else:
        tb.send_message(
            text=f'Envía la palabra "Cams" para habilitar las camaras"', chat_id=chat)
