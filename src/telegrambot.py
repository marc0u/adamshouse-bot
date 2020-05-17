import logging
import urllib.parse

import src.nettools as nt

class tb():
    def __init__(self, token_base):
        self.URL_BASE = f"https://api.telegram.org/bot{token_base}/"
        self._last_update_id = None
        
    def get_updates(self, offset=None) -> dict:
        url = self.URL_BASE + "getUpdates"
        if offset:
            url += "?offset={}".format(offset)
        js = nt.get_json_from_url(url)
        if js:
            return js
        else:
            logging.error('Updates json response could not be obtined.')
            return None

    def get_last_update_id(self, updates):
        if not updates or (not isinstance(updates, dict)):
            err = 'The "update" parameter is empty or is not dictionary type.'
            logging.error(err)
            raise AttributeError(err)
        if not updates['ok']:
            logging.error('The "ok" value si "False" from Telegram Updates response.')
            return False

        update_ids = []           
        for update in updates["result"]:
            update_ids.append(int(update["update_id"]))
        return max(update_ids)

    def get_last_chat_id_and_text(self, updates):
        if not updates or (not isinstance(updates, dict)):
            err = 'The "update" parameter is empty or is not dictionary type.'
            logging.error(err)
            raise AttributeError(err)
        if not updates['ok']:
            logging.error('The "ok" value si "False" from Telegram Updates response.')
            return False

        num_updates = len(updates["result"])
        last_update = num_updates - 1
        if 'edited_message' in updates["result"][last_update]:
            text = updates["result"][last_update]["edited_message"]["text"]
            chat_id = updates["result"][last_update]["edited_message"]["chat"]["id"]
            return (text, chat_id)
        else:
            text = updates["result"][last_update]["message"]["text"]
            chat_id = updates["result"][last_update]["message"]["chat"]["id"]
            return (text, chat_id)

    def get_updates_info(self, updates):
        if not updates or (not isinstance(updates, dict)):
            err = 'The "update" parameter is empty or is not dictionary type.'
            logging.error(err)
            raise AttributeError(err)
        if not updates['ok']:
            logging.error('The "ok" value si "False" from Telegram Updates response.')
            return False
            
        for update in updates["result"]:
            if 'edited_message' in update:
                text = update['edited_message']["text"]
                chat = update['edited_message']["chat"]["id"]
                user = update['edited_message']["from"]["id"]
            else:
                text = update["message"]["text"]
                chat = update["message"]["chat"]["id"]
                user = update["message"]["from"]["id"]
            yield (text, chat, user) 

    def send_message(self, text, chat_id):
        if (not isinstance(text, str)) or not chat_id:
            err = 'Problem with "text" or "chat_id" attribute.'
            logging.error(err)
            raise AttributeError(err)

        url = self.URL_BASE + "sendMessage?text={}&chat_id={}".format(text, chat_id)
        result = nt.get_url(url)
        if result:
            return True
        else:
            logging.error('Message cannot delivered')
            return False

    def bot_Handler(self, resp_handler):
        updates = self.get_updates(self._last_update_id)
        if not updates:
            logging.error('Updates response could not be obtined.')
            return False
        if not updates['ok']:
            logging.error('The "ok" value si "False" from Telegram Updates response.')
            return False
        if not len(updates["result"]) > 0:
            return True
        last_update_id_resp = self.get_last_update_id(updates)
        if not last_update_id_resp:
            logging.error('Last Update ID could not be obtined.')
            return False
        self._last_update_id = last_update_id_resp
        self._last_update_id += 1
        for update_info in self.get_updates_info(updates):
            if not update_info:
                logging.error('Updates info could not be obtined.')
                return False
            resp_handler(update_info)
        return True