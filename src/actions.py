from datetime import datetime
import re
from tendawifi import TendaAC15
from threading import Timer
from marcotools import retools
from marcotools.filestools import write_json_file, load_json_file
from time import sleep
from os import getenv
from reqtry import get

tenda = TendaAC15(password=getenv("TENDA_PASS"))
timer_cams = None
timer_vport = None


def get_time(tb_obj, chat):
    now = datetime.now()
    return tb_obj.send_message(text=now.strftime("%d/%m/%Y - %H:%M:%S"), chat_id=chat)

def get_public_ip(tb_obj, chat):
    return tb_obj.send_message(text=get("https://api.ipify.org").text, chat_id=chat)


def are_cams_alive(tb_obj, chat):
    global timer_cams
    try:
        if timer_cams.isAlive():
            return tb_obj.send_message(text='Enable', chat_id=chat)
        else:
            return tb_obj.send_message(text='Disable', chat_id=chat)
    except:
        return tb_obj.send_message(text='Disable', chat_id=chat)


def start_cams(tb_obj, chat, user_name, query, admin_id=None):
    res = re.match(
        r'(/startcams) (\b\d\d?\d?\d?\b)', query)
    if res == None:
        return tb_obj.send_message(text='Format not recognized. Ex. "/startcams alive_min:0-9999"', chat_id=chat)
    alive_min = res[2]
    global timer_cams
    macs = tenda.filter_bindlist_by_devname("C-")

    def set_cams_control(status) -> str:
        result = None
        for mac in macs:
            result = tenda.set_parent_control(mac['macaddr'], status)
        return result

    def cams_close():
        set_cams_control(1)
        return tb_obj.send_message(text='Time finished! Try sending "cams" for another 10 minutes.', chat_id=chat)

    if not set_cams_control(0):
        return tb_obj.send_message(text='Something wrong... It could not start the cameras.', chat_id=chat)
    try:
        timer_cams.cancel()
    except:
        pass
    timer_cams = Timer(int(alive_min)*60, cams_close)
    timer_cams.start()
    if admin_id:
        tb_obj.send_message(
            text=f'{user_name} has connected.', chat_id=admin_id)
    return tb_obj.send_message(text=f'Cams are enable for {alive_min} minutes.', chat_id=chat)


def add_vport(tb_obj, chat, query):
    res = re.match(
        r'(/addvport) (\b\d\d?\d?\b) (\b\d\d?\d?\d?\d?\b) (\b\d\d?\d?\d?\d?\b)', query)
    if res == None:
        return tb_obj.send_message(text='Format not recognized. Ex. "/addvport ip:1-254 inPort:0-65535 outPort:0-65535"', chat_id=chat)
    ip, inPort, outPort = res[2], res[3], res[4]
    vports = tenda.get_vports()
    if not vports:
        tb_obj.send_message(
            text='Something wrong... It could not get the vport list.', chat_id=chat)
        return
    vports["virtualList"].append(
        {'ip': "192.168.1."+ip, 'inPort': inPort, 'outPort': outPort, 'protocol': '0'})
    set_vport = tenda.set_vports(vports)
    if not set_vport:
        tb_obj.send_message(
            text='Something wrong... It could not set the vport list.', chat_id=chat)
        return
    tb_obj.send_message(text='Vport added successfully.', chat_id=chat)
    return set_vport


def remove_vport(tb_obj, chat, query):
    res = re.match(
        r'(/removevport) (\b\d\d?\d?\b) (\b\d\d?\d?\d?\d?\b) (\b\d\d?\d?\d?\d?\b)', query)
    if res == None:
        return tb_obj.send_message(text='Format not recognized. Ex. "/removevport ip:1-254 inPort:0-65535 outPort:0-65535"', chat_id=chat)
    ip, inPort, outPort = res[2], res[3], res[4]
    vports = tenda.get_vports()
    if not vports:
        tb_obj.send_message(
            text='Something wrong... It could not get the vport list.', chat_id=chat)
        return
    try:
        vports["virtualList"].remove(
            {'ip': "192.168.1."+ip, 'inPort': inPort, 'outPort': outPort, 'protocol': '0'})
    except ValueError:
        tb_obj.send_message(text='The vport is not in the list.', chat_id=chat)
        return
    set_vport = tenda.set_vports(vports)
    if not set_vport:
        tb_obj.send_message(
            text='Something wrong... It could not set the vport list.', chat_id=chat)
        return
    tb_obj.send_message(text='Vport removed successfully.', chat_id=chat)
    return set_vport


def start_vport(tb_obj, chat, query):
    res = re.match(
        r'(/startvport) (\b\d\d?\d?\b) (\b\d\d?\d?\d?\d?\b) (\b\d\d?\d?\d?\d?\b) (\b\d\d?\d?\d?\b)', query)
    if res == None:
        return tb_obj.send_message(text='Format not recognized. Ex. "/startvport ip:1-254 inPort:0-65535 outPort:0-65535 aliveMin:1-9999"', chat_id=chat)
    ip, inPort, outPort, alive_min = res[2], res[3], res[4], res[5]

    global timer_vport

    def vport_close():
        remove_vport(tb_obj, chat, f"/removevport {ip} {inPort} {outPort}")
        return tb_obj.send_message(text='Time finished! Vport is closed.',   chat_id=chat)

    if not add_vport(tb_obj, chat, f"/addvport {ip} {inPort} {outPort}"):
        return tb_obj.send_message(text='Something wrong... It could not start the Vport.', chat_id=chat)
    try:
        timer_vport.cancel()
    except:
        pass
    timer_vport = Timer(int(alive_min)*60, vport_close)
    timer_vport.start()
    return tb_obj.send_message(text=f'Vport is enable for {alive_min} minutes.', chat_id=chat)


def set_net_control(query, tb_obj=None, chat=None):
    res = re.match(
        r'(/net) (\b\d{1,4}\b) (\b\d{1,4}\b)\s?([w|b]-[A-Za-z0-9,_-]+)?\s?(\b\d{1,3}-\d{1,3}\b)?', query)
    if res == None:
        return tb_obj.send_message(text='Format not recognized. Ex. "/net up_limit:1-9999 down_limit:0-9999 (optional)white|black:w|b-aa,bb,cc ip_range:100-150"', chat_id=chat) if chat else None
    up, down, keywords, ip_range = res[2], res[3], res[4], res[5]
    if ip_range:
        ip_from, ip_to = ip_range.split("-")
        ip_from, ip_to = int(ip_from), int(ip_to)
        if ip_from > ip_to:
            return tb_obj.send_message(text='The first number of ip_range must be lower than the second. Ex. "ip_range:100-150"', chat_id=chat) if chat else None
    net = tenda.get_net_control()
    if not net:
        return tb_obj.send_message(text='Something wrong... It could not get the net control list.', chat_id=chat) if chat else None
    net_controled = [net[0]]
    devs_name = []
    for client in net[1:]:
        if keywords:
            keyword_list = keywords[2:].split(",")
            if keywords.startswith("b"):
                for item in keyword_list:
                    if item in client["hostName"]:
                        client["limitUp"] = up
                        client["limitDown"] = down
                        devs_name.append(client["hostName"])
                        break
            if keywords.startswith("w"):
                is_white = False
                for item in keyword_list:
                    if item in client["hostName"]:
                        is_white = True
                if not is_white:
                    client["limitUp"] = up
                    client["limitDown"] = down
                    devs_name.append(client["hostName"])
        if ip_range:
            ip = retools.all_after("192.168.1.", client["ip"])
            ip = int(ip) if ip else 0
            if ip_from <= ip <= ip_to:
                client["limitUp"] = up
                client["limitDown"] = down
                devs_name.append(client["hostName"])
        if not (keywords or ip_range):
            client["limitUp"] = up
            client["limitDown"] = down
            devs_name.append(client["hostName"])
        net_controled.append(client)
    if not tenda.set_net_control(net_controled):
        return tb_obj.send_message(text='Something wrong... It could not set the net control list.', chat_id=chat) if chat else None
    return tb_obj.send_message(text=f'Net control setted successfully uplimit: {up}kb/s downlimit: {down}kb/s for: {",".join(devs_name)}', chat_id=chat) if chat else None


def ofuscate(query, tb_obj=None, chat=None):
    res = re.match(
        r'(/ofuscate) (\b\d{1,4}\b) (\b\d{1,4}\b)\s?(\b\d{1,3}-\d{1,3}\b)?\s?([A-Za-z0-9,_-]+)?', query)
    if res == None:
        return tb_obj.send_message(text='Format not recognized. Ex. "/ofuscate how_many_times:1-9999" interval_sec:1-9999 ?target:someone ?ip_range:100-150', chat_id=chat, disable_notification=True) if chat else None
    how_many, interval_sec, ip_range, target, devs_name, to_ofuscate = int(
        res[2]), int(res[3]), res[4], res[5], [], []
    if ip_range:
        ip_from, ip_to = ip_range.split("-")
        to_ofuscate = tenda.filter_onlinelist_by_iprange(
            int(ip_from), int(ip_to))
    elif target:
        to_ofuscate = tenda.filter_onlinelist_by_devname(target)
    else:
        return tb_obj.send_message(text='target or ip_range are missing. It must exits one of them. Ex. "/ofuscate how_many_times:1-9999" interval_sec:1-9999 ?target:someone ?ip_range:100-150', chat_id=chat, disable_notification=True) if chat else None
    if not to_ofuscate:
        return tb_obj.send_message(text=f'Anyone match with: {target}' if target else f'Anyone is between {ip_range} ip range.', chat_id=chat, disable_notification=True) if chat else None
    devs_name = ",".join([item.get("devName", "")
                          for item in to_ofuscate])
    tb_obj.send_message(
        text=f'Ofuscating... "{devs_name}" for {how_many} times with intervals of {interval_sec} seconds.', chat_id=chat, disable_notification=True) if chat else None
    for _ in range(how_many):
        for dev in to_ofuscate:
            tenda.set_parent_control(dev["deviceId"], 1)
        sleep(interval_sec)
        for dev in to_ofuscate:
            tenda.set_parent_control(dev["deviceId"], 0)
        sleep(interval_sec)
    return tb_obj.send_message(text=f'"{devs_name}" were ofuscated for {how_many} times with intervals of {interval_sec} seconds.', chat_id=chat, disable_notification=True) if chat else None

def backup_ipmac_bind(tb_obj=None, chat=None):
    ipmac_bind = tenda.get_ipmac_bind()
    if not ipmac_bind:
        return tb_obj.send_message(text=f'Somthing wrong getting the ipmac list.', chat_id=chat, disable_notification=True) if chat else None
    if not write_json_file(ipmac_bind, "ipmac_bind.json"):
        return tb_obj.send_message(text=f'Somthing wrong saving the file "ipmac_bind.json".', chat_id=chat, disable_notification=True) if chat else None
    return tb_obj.send_message(text=f'Saved in "ipmac_bind.json".', chat_id=chat, disable_notification=True) if chat else None

def restore_ipmac_bind(tb_obj=None, chat=None):
    ipmac_bind = load_json_file("ipmac_bind.json")
    if not ipmac_bind:
        return tb_obj.send_message(text=f'Somthing wrong loading the file "ipmac_bind.json".', chat_id=chat, disable_notification=True) if chat else None
    tenda.set_ipmac_bind(ipmac_bind)
    return tb_obj.send_message(text=f'Restored from "ipmac_bind.json".', chat_id=chat, disable_notification=True) if chat else None