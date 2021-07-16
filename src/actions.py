from datetime import datetime
import re
from tendawifi import TendaAC15
from threading import Timer
from marcotools import retools
from time import sleep
from os import getenv

tenda = TendaAC15(password=getenv("TENDA_PASS"))
timer_cams = None
timer_vport = None


def get_time(tb_obj, chat):
    now = datetime.now()
    return tb_obj.send_message(now.strftime("%d/%m/%Y - %H:%M:%S"), chat)


def are_cams_alive(tb_obj, chat):
    global timer_cams
    try:
        if timer_cams.isAlive():
            return tb_obj.send_message('Enable', chat)
        else:
            return tb_obj.send_message('Disable', chat)
    except:
        return tb_obj.send_message('Disable', chat)


def start_cams(tb_obj, chat, user_name, query, admin_id=None):
    res = re.match(
        r'(/startcams) (\b\d\d?\d?\d?\b)', query)
    if res == None:
        return tb_obj.send_message('Format not recognized. Ex. "/startcams alive_min:0-9999"', chat)
    alive_min = res[2]
    global timer_cams
    macs = tenda.filter_bindlist_by_devname("c-")

    def set_cams_control(status) -> str:
        result = None
        for mac in macs:
            result = tenda.set_parent_control(mac['macaddr'], status)
        return result

    def cams_close():
        set_cams_control(1)
        return tb_obj.send_message('Time finished! Try sending "cams" for another 10 minutes.', chat)

    if not set_cams_control(0):
        return tb_obj.send_message('Something wrong... It could not start the cameras.', chat)
    try:
        timer_cams.cancel()
    except:
        pass
    timer_cams = Timer(int(alive_min)*60, cams_close)
    timer_cams.start()
    if admin_id:
        tb_obj.send_message(f'{user_name} has connected.', admin_id)
    return tb_obj.send_message(f'Cams are enable for {alive_min} minutes.', chat)


def add_vport(tb_obj, chat, query):
    res = re.match(
        r'(/addvport) (\b\d\d?\d?\b) (\b\d\d?\d?\d?\d?\b) (\b\d\d?\d?\d?\d?\b)', query)
    if res == None:
        return tb_obj.send_message('Format not recognized. Ex. "/addvport ip:1-254 inPort:0-65535 outPort:0-65535"', chat)
    ip, inPort, outPort = res[2], res[3], res[4]
    vports = tenda.get_vports()
    if not vports:
        tb_obj.send_message(
            'Something wrong... It could not get the vport list.', chat)
        return
    vports["virtualList"].append(
        {'ip': "192.168.1."+ip, 'inPort': inPort, 'outPort': outPort, 'protocol': '0'})
    set_vport = tenda.set_vports(vports)
    if not set_vport:
        tb_obj.send_message(
            'Something wrong... It could not set the vport list.', chat)
        return
    tb_obj.send_message(
        'Vport added successfully.', chat)
    return set_vport


def remove_vport(tb_obj, chat, query):
    res = re.match(
        r'(/removevport) (\b\d\d?\d?\b) (\b\d\d?\d?\d?\d?\b) (\b\d\d?\d?\d?\d?\b)', query)
    if res == None:
        return tb_obj.send_message('Format not recognized. Ex. "/removevport ip:1-254 inPort:0-65535 outPort:0-65535"', chat)
    ip, inPort, outPort = res[2], res[3], res[4]
    vports = tenda.get_vports()
    if not vports:
        tb_obj.send_message(
            'Something wrong... It could not get the vport list.', chat)
        return
    try:
        vports["virtualList"].remove(
            {'ip': "192.168.1."+ip, 'inPort': inPort, 'outPort': outPort, 'protocol': '0'})
    except ValueError:
        tb_obj.send_message(
            'The vport is not in the list.', chat)
        return
    set_vport = tenda.set_vports(vports)
    if not set_vport:
        tb_obj.send_message(
            'Something wrong... It could not set the vport list.', chat)
        return
    tb_obj.send_message(
        'Vport removed successfully.', chat)
    return set_vport


def start_vport(tb_obj, chat, query):
    res = re.match(
        r'(/startvport) (\b\d\d?\d?\b) (\b\d\d?\d?\d?\d?\b) (\b\d\d?\d?\d?\d?\b) (\b\d\d?\d?\d?\b)', query)
    if res == None:
        return tb_obj.send_message('Format not recognized. Ex. "/startvport ip:1-254 inPort:0-65535 outPort:0-65535 aliveMin:1-9999"', chat)
    ip, inPort, outPort, alive_min = res[2], res[3], res[4], res[5]

    global timer_vport

    def vport_close():
        remove_vport(tb_obj, chat, f"/removevport {ip} {inPort} {outPort}")
        return tb_obj.send_message('Time finished! Vport is closed.', chat)

    if not add_vport(tb_obj, chat, f"/addvport {ip} {inPort} {outPort}"):
        return tb_obj.send_message('Something wrong... It could not start the Vport.', chat)
    try:
        timer_vport.cancel()
    except:
        pass
    timer_vport = Timer(int(alive_min)*60, vport_close)
    timer_vport.start()
    return tb_obj.send_message(f'Vport is enable for {alive_min} minutes.', chat)


def set_net_control(query, tb_obj=None, chat=None):
    res = re.match(
        r'(/net) (\b\d\d?\d?\d?\b) (\b\d\d?\d?\d?\b)\s?([w|b]-[A-Za-z0-9,_-]+)?\s?(\b\d\d?\d?-\d\d?\d?\b)?', query)
    if res == None:
        return tb_obj.send_message('Format not recognized. Ex. "/net up_limit:1-9999 down_limit:0-9999 (optional)white|black:w|b-aa,bb,cc ip_range:100-150"', chat) if chat else None
    up, down, keywords, ip_range = res[2], res[3], res[4], res[5]
    if ip_range:
        ip_from, ip_to = ip_range.split("-")
        ip_from, ip_to = int(ip_from), int(ip_to)
        if ip_from > ip_to:
            return tb_obj.send_message('The first number of ip_range must be lower than the second. Ex. "ip_range:100-150"', chat) if chat else None
    net = tenda.get_net_control()
    if not net:
        return tb_obj.send_message('Something wrong... It could not get the net control list.', chat) if chat else None
    net_controled = [net[0]]
    for client in net[1:]:
        if keywords:
            keyword_list = keywords[2:].split(",")
            if keywords.startswith("b"):
                for item in keyword_list:
                    if item in client["hostName"]:
                        print(client["hostName"])
                        client["limitUp"] = up
                        client["limitDown"] = down
                        break
            if keywords.startswith("w"):
                is_white = False
                for item in keyword_list:
                    if item in client["hostName"]:
                        is_white = True
                if not is_white:
                    print(client["hostName"])
                    client["limitUp"] = up
                    client["limitDown"] = down
        if ip_range:
            ip = retools.all_after("192.168.1.", client["ip"])
            ip = int(ip) if ip else 0
            if ip_from <= ip <= ip_to:
                client["limitUp"] = up
                client["limitDown"] = down
        if not (keywords or ip_range):
            print(client["hostName"])
            client["limitUp"] = up
            client["limitDown"] = down
        net_controled.append(client)
    set_net = tenda.set_net_control(net_controled)
    if not set_net:
        return tb_obj.send_message('Something wrong... It could not set the net control list.', chat) if chat else None
    return tb_obj.send_message('Net control setted successfully.', chat) if chat else None


def ofuscate(query, tb_obj=None, chat=None):
    res = re.match(
        r'(/ofuscate) (.*) (\b\d\d?\d?\d?\b) (\b\d\d?\d?\d?\b)', query)
    if res == None:
        return tb_obj.send_message('Format not recognized. Ex. "/ofuscate someone how_many:1-9999" interval_sec:1-9999', chat) if chat else None
    targets = tenda.filter_onlinelist_by_devname(res[2])
    how_many, interval_sec = int(res[3]), int(res[4])
    for _ in range(how_many):
        for target in targets:
            tenda.set_parent_control(target["deviceId"], 1)
        sleep(interval_sec)
        for target in targets:
            tenda.set_parent_control(target["deviceId"], 0)
        sleep(interval_sec)
