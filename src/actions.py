import logging
import re
from tendawifi import TendaAC15
from threading import Timer

tenda = TendaAC15(password="9467804")
timer_cams = None
timer_vport = None


def are_cams_alive(tb_obj, chat):
    global timer_cams
    try:
        if timer_cams.isAlive():
            return tb_obj.send_message('Enable', chat)
        else:
            return tb_obj.send_message('Disable', chat)
    except:
        return tb_obj.send_message('Disable', chat)


def start_cams(tb_obj, chat, user_name, alive_min=10, admin_id=None) -> bool:
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
    timer_cams = Timer(int(alive_min*60), cams_close)
    timer_cams.start()
    if admin_id:
        tb_obj.send_message(f'{user_name} has connected.', admin_id)
    return tb_obj.send_message(f'Cams are enable for {alive_min} minutes.', chat)


def add_vport(tb_obj, chat, query):
    res = re.match(
        r'(/addvport) (\d\d*\d*) (\b\d\d?\d?\d?\d?\b) (\b\d\d?\d?\d?\d?\b)', query)
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
        r'(/removevport) (\d\d*\d*) (\b\d\d?\d?\d?\d?\b) (\b\d\d?\d?\d?\d?\b)', query)
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
        r'(/startvport) (\d\d*\d*) (\b\d\d?\d?\d?\d?\b) (\b\d\d?\d?\d?\d?\b) (\b\d\d?\d?\d?\b)', query)
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


# def netcontrol(up, down, tb_obj=None, chat=None):
#    static = "\nGloria-TV\r10:08:c1:a4:cf:22\r50\r300\nGloria-Phone\rd0:13:fd:2f:d1:c7\r50\r300\nQuelo-Phone\r3c:fa:43:19:7b:0e\r50\r300\nQuelo-Tablet\r7c:46:85:50:2c:ab\r50\r300"
#    data = f"list=Isi%20tv\r10:c7:53:34:9d:06\r{up}\r{down}\nI-iPad\r3c:15:c2:15:03:aa\r{up}\r{down}\nIsi's%20Phone\r74:c1:4f:7b:93:f6\r{up}\r{down}\nI-Laptop\rb4:82:fe:3f:75:6e\r{up}\r{down}\nI-Phone-New\r10:32:7e:87:ce:b7\r{up}\r{down}\nI-Unknown\r58:2f:40:7a:e9:3a\r{up}\r{down}\nLiving-TV\rd8:e0:e1:3e:54:1c\r{up}\r{down}\nI-Laptop-Hp\r4c:eb:bd:69:dd:d5\r{up}\r{down}" + static
#    if tenda.set_net_control(data):
#         if tb_obj:
#             return tb_obj.send_message(f'Net Control setted in upload: {up}k/s and download: {down}k/s.', chat)
#         else:
#             return True
#     else:
#         if tb_obj:
#             return tb_obj.send_message('It could not set Net Control.', chat)
#         else:
#             return False

# def start_torrent(tb_obj, chat, query):
#     res = re.match(r'(/torrent) (\b\d\d?\d?\d?\b)', query)
#     if res == None:
#         return tb_obj.send_message('Format not recognized. Ex. "/torrent aliveMin"', chat)
#     try:
#         ip, inPort, outPort, alive_min = '192.168.1.15', '9091', '999', res[2]

#         def close_msg(status):
#             if not status:
#                 return tb_obj.send_message('Something wrong... "torrent" could not be stopped!', chat)
#             return tb_obj.send_message('"torrens" Stopped.', chat)
#         if not tenda.start_vport(ip, inPort, outPort, alive_min, close_fuc=close_msg):
#             return tb_obj.send_message('Something wrong... It could not start "torrent".', chat)
#         # Successful return
#         return tb_obj.send_message('"torrens" Started.', chat)
#     except Exception:
#         logging.exception("Exception occurred")
#         return tb_obj.send_message('Something wrong... It could not start "torrent".', chat)


# def proxmox(tb_obj, chat, query):
#     res = re.match(r'(/proxmox) (\b\d\d?\d?\d?\b)', query)
#     if res == None:
#         return tb_obj.send_message('Format not recognized. Ex. "/proxmox aliveMin"', chat)
#     try:
#         ip, inPort, outPort, alive_min = '192.168.1.10', '8006', '888', res[2]

#         def close_msg(status):
#             if not status:
#                 return tb_obj.send_message('Something wrong... "proxmox" could not be stopped!', chat)
#             return tb_obj.send_message('"proxmox" Stopped.', chat)
#         if not tenda.start_vport(ip, inPort, outPort, alive_min, close_fuc=close_msg):
#             return tb_obj.send_message('Something wrong... It could not start "proxmox".', chat)
#         # Successful return
#         return tb_obj.send_message('"proxmox" Started.', chat)
#     except Exception:
#         logging.exception("Exception occurred")
#         return tb_obj.send_message('Something wrong... It could not start "proxmox".', chat)


# def add_vport(self, ip: str, inPort: int, outPort: int, protocol='0') -> str:
#     vports_list = self.parse_vports_list(self.get_vports())
#     if not vports_list:
#         logger.warn("vport_list variable is empty.")
#         return
#     sep1, sep2 = ',', '~'
#     vport_to_add = sep2 + ip + sep1 + \
#         str(inPort) + sep1 + str(outPort) + sep1 + protocol
#     if vport_to_add in vports_list:
#         logger.debug(
#             f'Virtual Port already in the list: IP:{ip} InPort:{inPort} OutPort:{outPort}')
#         return f'Virtual Port already in the list: IP:{ip} InPort:{inPort} OutPort:{outPort}'
#     vports_list += vport_to_add
#     return self.set_vports(vports_list)

# def remove_vport(self, ip: str, inPort: int, outPort: int, protocol='0') -> str:
#     vports_list = self.parse_vports_list(self.get_vports())
#     if not vports_list:
#         logger.warn("vport_list variable is empty.")
#         return
#     sep1, sep2 = ',', '~'
#     vport_to_remove = sep2 + ip + sep1 + \
#         str(inPort) + sep1 + str(outPort) + sep1 + protocol
#     if not vport_to_remove in vports_list:
#         logger.debug(
#             f'Virtual Port is not in the current list: IP:{ip} InPort:{inPort} OutPort:{outPort}')
#         return f'Virtual Port already in the list: IP:{ip} InPort:{inPort} OutPort:{outPort}'
#     vports_list = vports_list.replace(vport_to_remove, '')
#     return self.set_vports(vports_list)

# def open_vport_timer(self, ip: str, inPort: int, outPort: int, alive_min: int, protocol='0', close_func=None) -> bool:
#     def close():
#         if self.remove_vport(ip, inPort, outPort, protocol):
#             if close_func:
#                 close_func(True)
#         else:
#             if close_func:
#                 close_func(False)
#     if not self.add_vport(ip, inPort, outPort, protocol):
#         return False
#     vport = Timer(alive_min*60, close)
#     vport.start()
#     return True
