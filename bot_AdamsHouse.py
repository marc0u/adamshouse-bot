# Load vatiablers from .env file
from dotenv import load_dotenv, find_dotenv
try:
    load_dotenv(find_dotenv(raise_error_if_not_found=True), override=True)
except:
    raise
else:
    import logging
    from os import getenv
    from threading import Thread
    from src.botloop import Bot
    from src.netloop import NetControl

# Logging
filename = getenv("HOME") + "/logs/" + "AdamsHouse" + ".log"
logging.basicConfig(filename=filename, format='%(asctime)s - %(levelname)s / %(module)s / %(funcName)s / %(message)s',
                    datefmt='%H:%M:%S', level=logging.ERROR)

logging.error("Hello world")
if __name__ == "__main__":
    Thread(target=Bot).start()
    Thread(target=NetControl).start()
