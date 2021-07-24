from os import getenv


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
