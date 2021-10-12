from tendawifi import TendaAC15
from os import getenv
from marcotools.filestools import load_json_file

tenda = TendaAC15(password=getenv("TENDA_PASS"))


def setup_router():
    tenda.set_fast_internet(getenv("TENDA_MAC"))
    tenda.set_fast_router(getenv("TENDA_SSID"), getenv(
        "TENDA_WIFI_PASS"), getenv("TENDA_PASS"))


def setup_wifi():
    tenda.setup_wifi(getenv("TENDA_SSID"), getenv("TENDA_WIFI_PASS"))
    tenda.set_autoreboot_status(0)
    tenda.set_wps_status(0)


def restore_ipmac_bind():
    ipmac_bind = load_json_file("ipmac_bind.json")
    assert ipmac_bind, 'Somthing wrong loading the file "ipmac_bind.json"'
    tenda.set_ipmac_bind(ipmac_bind)
