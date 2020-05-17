import json
import logging
import time
from threading import Timer

import src.generaltools as gt
import src.nettools as nt


class tenda(nt.AuthSession):
    _URL_BASE = 'http://localhost:8080'
    # _URL_BASE = 'http://192.168.1.1'
    _URLS = {
        'login': _URL_BASE+'/login/Auth',
        'GetParentControl': _URL_BASE+'/goform/GetParentControlInfo?mac=',
        'SetParentControl': _URL_BASE+'/goform/parentControlEn',
        'GetVports': _URL_BASE+'/goform/GetVirtualServerCfg',
        'SetVports': _URL_BASE+'/goform/SetVirtualServerCfg',
        'SetNetControl': _URL_BASE+'/goform/SetNetControlList'
        }
    _AUTH_URL = _URLS['login']
    _AUTH_DATA = {'username': 'admin','password': '597e53ec61d987a3e488f7d42c01d9c3'}
    MACS_CAMS = {
        'nvr':'00:12:17:a2:38:33',
        'cam':'30:ff:f6:31:1f:9b'
        }
    MACS_SERVER = {
        'webhost':'4a:4b:cc:7b:ce:aa',
        'proxmox':'74:46:a0:cb:1c:12'
        }
    vports_list = ''
    _timer_cams = None

    def get_setting(self, url):
        resp = self.get_json(url, allow_redirects=False, timeout=self._timeout)
        if resp == None:
            return None
        return resp

    def set_setting(self, url, data) -> bool:
        resp = self.post(url, data=data, allow_redirects=False, timeout=self._timeout)
        if resp == None:
            return False
        if resp.status_code != 200:
            err = 'Http status code is not "200". It is: ' + str(resp.status_code)
            logging.error(err)
            return False
        if '0' not in str(resp):
            logging.error('It could not set setting.')
            return False
        logging.info(f'Setting successfully set.')
        return True

    def get_parent_control(self, mac:str) -> dict:
        resp = self.get_setting(self._URLS['GetParentControl'] + mac)
        if resp == None:
            logging.error("It could not get parent control.")
            return None
        return resp

    def set_parent_control(self, mac:str, status:int) -> bool:
        if not self.set_setting(self._URLS['SetParentControl'], data={'mac': mac, 'isControled': status}):
            logging.error('It could not set parent control.')
            return False
        logging.info(f'Parent control was setted to "{status}" for mac:"{mac}".')
        return True

    def get_vports(self) -> bool:
        resp = self.get_setting(self._URLS['GetVports'])
        if not resp:
            logging.error("It could not get Virtual Ports.")
            return False
        try:
            vports_list = resp['virtualList']
            vports_list_formated = []
            sep1, sep2 = ',' , '~'
            for vport in vports_list:
                vports_list_formated.append(vport['ip'] + sep1 + vport['inPort'] + sep1 + vport['outPort'] + sep1 + vport['protocol'])
            self.vports_list = sep2.join(vports_list_formated)
            return True
        except Exception:
            logging.exception("Exception occurred")
            self.vports_list = ''
            return False

    def add_vport(self, ip, inPort, outPort, protocol='0') -> bool:
        if not self.get_vports():
            return False
        sep1, sep2 = ',' , '~'
        vport_to_add = sep2 + ip + sep1 + inPort + sep1 + outPort + sep1 + protocol
        if vport_to_add in self.vports_list:
            logging.info(f'Virtual Port already Added: IP:"{ip}" InPort:"{inPort}" OutPort:"{outPort}".')
            return True
        self.vports_list += vport_to_add
        if not self.set_setting(self._URLS['SetVports'], data={'list':self.vports_list}):
            self.vports_list = ''
            logging.error("It could not add the Virtual Port requested.")
            return False
        logging.info(f'Virtual Port Added: IP:"{ip}" InPort:"{inPort}" OutPort:"{outPort}".')
        return True

    def remove_vport(self, ip, inPort, outPort, protocol='0') -> bool:
        if not self.get_vports():
            return False
        sep1, sep2 = ',' , '~'
        vport_to_remove = sep2 + ip + sep1 + inPort + sep1 + outPort + sep1 + protocol
        if not vport_to_remove in self.vports_list:
            logging.error("Virtual Port is not in the actual Virtual Port List.")
            return False
        self.vports_list = self.vports_list.replace(vport_to_remove, '')
        if not self.set_setting(self._URLS['SetVports'], data={'list':self.vports_list}):
            self.vports_list = ''
            logging.error("It could not remove the Virtual Port requested.")
            return False
        logging.info(f'Virtual Port Removed: IP:"{ip}" InPort:"{inPort}" OutPort:"{outPort}."')
        return True

    def start_vport(self, ip, inPort, outPort, alive_min, protocol='0', close_fuc=None) -> bool:
        def close():
            if self.remove_vport(ip, inPort, outPort, protocol):
                if close_fuc:
                    close_fuc(True)
            else:
                if close_fuc:
                    close_fuc(False)
        if not self.add_vport(ip, inPort, outPort, protocol):
            return False
        alive_min = int(alive_min)*60
        vport = Timer(alive_min, close)
        vport.start()
        return True
    
    def are_cams_alive(self) -> bool:
        try:
            if self._timer_cams.isAlive():
                return True
            else:
                return False
        except:
            return False
    
    def start_cams(self, alive_min, close_msg=None) -> bool:
        def cams_close(close_msg=None) -> None:
            self.set_parent_control(self.MACS_CAMS['nvr'], 1)
            self.set_parent_control(self.MACS_CAMS['cam'], 1)
            if close_msg:
                close_msg()
        nvr = self.set_parent_control(self.MACS_CAMS['nvr'], 0)
        cam = self.set_parent_control(self.MACS_CAMS['cam'], 0)
        if not nvr and not cam:
            return False
        alive_min = int(alive_min*60)
        try:
            self._timer_cams.cancel()
        except:
            pass
        self._timer_cams = Timer(alive_min, cams_close, args=[close_msg])
        self._timer_cams.start()
        return True
    
    def set_net_control(self, data_list) -> bool:
        if not self.set_setting(self._URLS['SetNetControl'], data=data_list):
            logging.error('It could not set net control.')
            return False
        logging.info('Net control was setted.')
        return True