import logging
import re

import src.tenda as td

tenda = td.tenda()

def camstart(tb_obj, chat, user_name, admin_id=None):
    alive_min = 10
    def close_msg():
        return tb_obj.send_message('Time finished! Try sending "cams" for another 10 minutes.', chat)
    if not tenda.start_cams(alive_min, close_msg):
        return tb_obj.send_message('Something wrong... It could not start the cameras.', chat)
    if admin_id:
        tb_obj.send_message(f'{user_name} has connected.', admin_id)
    return tb_obj.send_message(f'Cams are enable for {alive_min} minutes.', chat)
    
def camstatus(tb_obj, chat):
    if tenda.are_cams_alive():
        return tb_obj.send_message('Enable', chat)
    else:
        return tb_obj.send_message('Disable', chat)

def startvport(tb_obj, chat, query):
    res = re.match(r'(/startvport) (192.168.1.\d\d*\d*) (\b\d\d?\d?\d?\d?\b) (\b\d\d?\d?\d?\d?\b) (\b\d\d?\d?\d?\b)', query)
    if res == None:
        return tb_obj.send_message('Format not recognized. Ex. "/startvport ip inPort outPort aliveMin"', chat)
    try:
        ip, inPort, outPort, alive_min = res[2], res[3], res[4], res[5]
        def close_msg(status):
            if not status:
                return tb_obj.send_message(f'Virtual Port could not be removed: \nIP:"{ip}" \nInPort:"{inPort}" \nOutPort:"{outPort}"', chat)
            return tb_obj.send_message(f'Virtual Port Removed: \nIP:"{ip}" \nInPort:"{inPort}" \nOutPort:"{outPort}"', chat)
        if not tenda.start_vport(ip, inPort, outPort, alive_min, close_fuc=close_msg):
            return tb_obj.send_message('Something wrong... It could not start the vport.', chat)
        ## Successful return
        return tb_obj.send_message(f'Virtual Port Started for {alive_min} min: \nIP:"{ip}" \nInPort:"{inPort}" \nOutPort:"{outPort}"', chat)
    except Exception:
        logging.exception("Exception occurred")
        return tb_obj.send_message('Something wrong... It could not start the vport.', chat)

def start_torrent(tb_obj, chat, query):
    res = re.match(r'(/torrent) (\b\d\d?\d?\d?\b)', query)
    if res == None:
        return tb_obj.send_message('Format not recognized. Ex. "/torrent aliveMin"', chat)
    try:
        ip, inPort, outPort, alive_min = '192.168.1.15', '9091', '999', res[2]
        def close_msg(status):
            if not status:
                return tb_obj.send_message('Something wrong... "torrent" could not be stopped!', chat)
            return tb_obj.send_message('"torrens" Stopped.', chat)
        if not tenda.start_vport(ip, inPort, outPort, alive_min, close_fuc=close_msg):
            return tb_obj.send_message('Something wrong... It could not start "torrent".', chat)
        ## Successful return
        return tb_obj.send_message('"torrens" Started.', chat)
    except Exception:
        logging.exception("Exception occurred")
        return tb_obj.send_message('Something wrong... It could not start "torrent".', chat)

def proxmox(tb_obj, chat, query):
    res = re.match(r'(/proxmox) (\b\d\d?\d?\d?\b)', query)
    if res == None:
        return tb_obj.send_message('Format not recognized. Ex. "/proxmox aliveMin"', chat)
    try:
        ip, inPort, outPort, alive_min = '192.168.1.10', '8006', '888', res[2]
        def close_msg(status):
            if not status:
                return tb_obj.send_message('Something wrong... "proxmox" could not be stopped!', chat)
            return tb_obj.send_message('"proxmox" Stopped.', chat)
        if not tenda.start_vport(ip, inPort, outPort, alive_min, close_fuc=close_msg):
            return tb_obj.send_message('Something wrong... It could not start "proxmox".', chat)
        ## Successful return
        return tb_obj.send_message('"proxmox" Started.', chat)
    except Exception:
        logging.exception("Exception occurred")
        return tb_obj.send_message('Something wrong... It could not start "proxmox".', chat)

def netcontrol(up, down, tb_obj=None, chat=None):
    static = "\nGloria-TV\r10:08:c1:a4:cf:22\r50\r300\nGloria-Phone\rd0:13:fd:2f:d1:c7\r50\r300\nQuelo-Phone\r3c:fa:43:19:7b:0e\r50\r300\nQuelo-Tablet\r7c:46:85:50:2c:ab\r50\r300"
    data = f"list=Isi%20tv\r10:c7:53:34:9d:06\r{up}\r{down}\nI-iPad\r3c:15:c2:15:03:aa\r{up}\r{down}\nIsi's%20Phone\r74:c1:4f:7b:93:f6\r{up}\r{down}\nI-Laptop\rb4:82:fe:3f:75:6e\r{up}\r{down}\nI-Phone-New\r10:32:7e:87:ce:b7\r{up}\r{down}\nI-Unknown\r58:2f:40:7a:e9:3a\r{up}\r{down}\nLiving-TV\rd8:e0:e1:3e:54:1c\r{up}\r{down}\nI-Laptop-Hp\r4c:eb:bd:69:dd:d5\r{up}\r{down}" + static
    if tenda.set_net_control(data):
        if tb_obj:
            return tb_obj.send_message(f'Net Control setted in upload: {up}k/s and download: {down}k/s.', chat)
        else:
            return True
    else:
        if tb_obj:
            return tb_obj.send_message('It could not set Net Control.', chat)
        else:
            return False