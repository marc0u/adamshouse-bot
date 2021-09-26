from os import getenv
import functools


def assert_envs():
    assert getenv("TB_TOKEN"), "'TB_TOKEN' enviroment variable is missing"
    assert getenv(
        "LOGGER_TB_TOKEN"), "'LOGGER_TB_TOKEN' enviroment variable is missing"
    assert getenv(
        "LOGGER_TB_CHAT_ID"), "'LOGGER_TB_CHAT_ID' enviroment variable is missing"


def parse_ip_range(tb_obj, chat, ip_range_str):
    if ip_range_str:
        ip_from, ip_to = ip_range_str.split("-")
        ip_from, ip_to = int(ip_from), int(ip_to)
        if ip_from > ip_to:
            tb_obj.send_message(
                text='The first number of ip_range must be lower than the second. Ex. "ip_range:100-150"', chat_id=chat) if chat else None
            return None, None
        return ip_from, ip_to


def with_err_resp(func):
    """Send telegram message response if an error occurred.
    :param func: func(tb_obj, chat, *args, **kwargs)
    """
    @functools.wraps(func)
    def wrapper(tb_obj, chat, *args, **kwargs):
        try:
            return func(tb_obj, chat, *args, **kwargs)
        except Exception as e:
            return tb_obj.send_message(text=str(e), chat_id=chat, disable_notification=True) if chat else None
    return wrapper
