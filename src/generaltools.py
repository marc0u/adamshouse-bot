import json
import datetime
import logging

from functools import wraps
from time import sleep

def with_retry(retries_and_sleep):
    retries, sleep_sec = retries_and_sleep or (3, 1)
    def real_decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            # print(f'Retries: {retries}')
            for _ in range(retries):
                # print(f'Retry: {x+1}')
                result = function(*args, **kwargs)
                if result:
                    return result
                sleep(sleep_sec)
        return wrapper
    return real_decorator

def msg_maker(*argv) -> str:
    msg = ""
    for arg in argv:
        msg += arg + "\n"
    return msg

def msg_maker_dic(dic) -> str:
    msg = ''
    for key, value in dic.items():
        msg = f'{key}: {value}\n' + msg
    return msg

def now_log(log) -> str:
    now = datetime.datetime.now()
    now = now.strftime("%m/%d/%Y - %H:%M:%S >> ") + log
    return now

def json_to_dict(json_str:str) -> dict:
    try:
        return json.loads(json_str)
    except:
        logging.error("The argument has not json format.")
        return None

def datetime_to_str(datetimeobj) -> str:
    if isinstance(datetimeobj, datetime.datetime):
        return datetimeobj.__str__()

def json_to_file(pyton_dic:dict, file_name:str) -> bool:
    """Generate a file.json from a python dictionary.
    ex. json_to_file(pyton_dictionary ,'c:\\file.json')
    """
    try:
        with open(file_name, 'w') as fp:
            json.dump(pyton_dic, fp, indent=4, default=datetime_to_str)
        return True
    except Exception:
        logging.exception("Exception occurred")
        return False

def json_from_file(file) -> dict:
    data = None
    try:
        with open(file) as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        logging.error(f'Json file "{file}" not found.')
        return None