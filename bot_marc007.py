import logging
from time import sleep
import os.path

import m_entel
import m_log
import m_nettools as nt
import m_sc
import m_telegramBot

tb = m_telegramBot.tb('856967587:AAEVWjlNNolEJBNp1gBHopkppTrLXcvBGig')
sc = m_sc.sc()
entel = m_entel.entel()
filename = os.path.basename(__file__)
m_log.log_start(filename)

def resp_handler(update_info):
    text, chat, user = update_info
    def admin(user):
        if text == "/ip":
            logging.info(f'{user[1]} has requested current IP.')
            ip = nt.get_url('https://api.ipify.org')
            tb.send_message("My ip is: {}".format(ip), user[0])
        elif text == "/sc":
            logging.info(f'{user[1]} has requested Sc info.')
            sc.refresh()
            tb.send_message(sc.report, user[0])
        elif text == "/entel":
            logging.info(f'{user[1]} has requested Entel info.')
            entel.refresh()
            tb.send_message(entel.report, user[0])
        else:
            tb.send_message("I'm not recognize that command!", user[0])

    if user == tb.admin[0]:
        admin(tb.admin)
    else:
        logging.warning('Someone strange is trying to connect with the bot.')
        tb.send_message('WARNING: Someone strange is trying to connect with the bot.', tb.admin[0])
        tb.send_message('Username wrong!', chat)

logging.info('bot_marc007 is running!')
while True:
    try:
        tb.bot_Handler(resp_handler)
        sleep(1.0)
    except Exception:
        logging.exception("Exception occurred")
        sleep(10.0)