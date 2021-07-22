# Load vatiablers from .env file
from dotenv import load_dotenv, find_dotenv
try:
    load_dotenv(find_dotenv(raise_error_if_not_found=True), override=True)
except:
    raise
else:
    from os import getenv
    from threading import Thread
    from src.botloop import Bot
    from src.netloop import NetControl
    from src.logger import init_logger
    from src.utils import assert_envs


assert_envs()
logger = init_logger("adamshousebot", getenv("DEBUG"))

if __name__ == "__main__":
    Thread(target=Bot).start()
    Thread(target=NetControl).start()
