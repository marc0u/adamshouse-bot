from tendawifi import TendaAC15
from os import getenv

tenda = TendaAC15(password=getenv("TENDA_PASS"))


def setup_internet():
    assert '"errCode":0' in tenda.set_fast_internet(
        getenv("TENDA_MAC")), "Could not setup internet."


def setup_router():
    assert '"errCode":0' in tenda.set_fast_router(getenv("TENDA_SSID"), getenv(
        "TENDA_WIFI_PASS"), getenv("TENDA_PASS")), "Could not setup router."


def setup_securities():
    tenda.set_autoreboot_status(0)
    tenda.set_wps_status(0)
