import m_generalTools as tt
import m_nettools as nt
import json
import logging

class sc(nt.session):
    _auth_url = 'https://www.scotiabank.cl/cgi-bin/transac/login-scotiaweb'
    _auth_data = {
        'rut': '0172829295',
        'usu': '0172829295',
        'pin': 'AIARA2911',
        'TRANS': 'vt_logon',
        'Validate_rut': '17.282.929-5'
    }
    urls = {'balances':'https://www.scotiabank.cl/cgi-bin/transac/dotrxajax?TMPL=%2Fadmin%2Fposicion.json&TRANS=vt_posicion&data=CTA002000000973375091000974105098'}

    def __init__(self):
        self.balance = 'Not refreshed!'
        self.cta_cte = 'Not refreshed!'
        self.cta_cte_num = 'Not refreshed!'
        self.cta_renta = 'Not refreshed!'
        self.cta_renta_num = 'Not refreshed!'
        self.report = 'Not refreshed!'
        self.c_cards = [ 'Not' , 'refreshed!']

    def refresh(self):
        def get(session):
            resp = session.get(self.urls['balances'], timeout=self._timeout)
            if resp.status_code >= 400:
                return False
            try:
                self.balance = json.loads(resp.text)
                self.cta_cte = self.get_float_str(self.balance["lstPosicion"]["cuentas"][0]["mtopricta"])
                self.cta_renta = self.get_float_str(self.balance["lstPosicion"]["cuentas"][2]["mtopricta"])
                self.lc = self.get_float_str(self.balance["lstPosicion"]["cuentas"][1]["mtopricta"])
                self.report = tt.msg_maker(
                    'CC: ' + self.cta_cte[1],
                    'CR: ' + self.cta_renta[1],
                    'LC: ' + self.lc[1]
                )
                return True
            except Exception:
                logging.exception("Exception occurred")
                return None
        self.auth_session(get)

    def credit_cards(self):
        def get_cards(session):
            list_cards = json.loads(session.get('https://www.scotiabank.cl/cgi-bin/transac/dotrxajax?TMPL=%2Fvisa%2FlstTarjetaSaldosEnc.json', timeout=self._timeout).text)
            code = list_cards["L09000"]["cards"][0]["prdoriid"]
            return [f'https://www.scotiabank.cl/cgi-bin/transac/dotrxajax?TMPL=%2Fvisa%2FsaldoLeapEnc.json&TRANS=vt_NuevoSaldoVisaEnc&visa={code}']
             
        def get(session):
            print('Point 1')
            for url in url_c_cards:
                print('Point 2')
                balance = session.get(url, timeout=self._timeout)
                print(balance.text)
                if balance.status_code < 400:
                    balance = json.loads(balance.text)
                    balance = balance["lstNuevoSaldoVisaEnc"]
                    c_card_num = balance["numeroTarjeta"]
                    c_card_nat_used = self.get_float_str(balance["cupoUtilizadoNacional"])
                    c_card_int_used = self.get_float_str(balance["cupoUtilizadoInternacional"])
                    c_card_result = {'cc_num':c_card_num, 'cc_nat_used':c_card_nat_used, 'cc_int_used':c_card_int_used}

                    self.c_cards['ok'] = True
                    self.c_cards['cc'].append(c_card_result)
                else:          
                    return 'Problem geting accounts balances!'
        url_c_cards = self.auth_session(get_cards)
        self.c_cards = {'ok':False, 'cc':[]}
        self.auth_session(get)   

    def get_float_str(self, str_number):
        num_float = float(str_number) / 100
        num_str = str(f'{num_float:,.0f}').replace(',', '.')
        return [num_float, num_str]

# s = sc()
# s.refresh()
# print(s.report)