from os import getenv


def assert_envs():
    assert getenv("TB_TOKEN"), "'TB_TOKEN' enviroment variable is missing"
    assert getenv("LOGGER_TB_TOKEN"), "'LOGGER_TB_TOKEN' enviroment variable is missing"
    assert getenv("LOGGER_TB_CHAT_ID"), "'LOGGER_TB_CHAT_ID' enviroment variable is missing"