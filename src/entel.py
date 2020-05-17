import json
import m_nettools as nt
import m_generalTools as tt

class entel(nt.session):
    _auth_url = 'https://miportal.entel.cl/oam/server/authentication'
    _auth_data = {
        'username': '56978074518',
        'rutt': '17927721-2',
        'password': '6274',
        'successurl': 'https://miportal.entel.cl/api/oamCallBack'
    }

    def __init__(self):
        self.balance = {'success': False}
        self.consumption = {'success': False}
        self.days = 'Not refreshed!'
        self.sms = 'Not refreshed!'
        self.voice = 'Not refreshed!'
        self.data = 'Not refreshed!'
        self.report = 'Not refreshed!'

    def refresh(self):
        def get(session):
            self.balance = session.get('https://miportal.entel.cl/restpp/asset/accountBalance', timeout=(3, 5))
            self.consumption = session.get('https://miportal.entel.cl/restpp/asset/consumptionInfo', timeout=(3, 5))
            self.balance = json.loads(self.balance.text)
            self.consumption = json.loads(self.consumption.text)
            if self.balance['success']:
                self.remaingBalance = self.balance['response']['balance']['remaingBalance']
            else:
                self.remaingBalance = 'Remaing balance Error!'
            if self.consumption['success']:
                self.days = self.consumption['response']['consumption']['refreshDays']
                self.sms = [self.consumption['response']['consumption']['usedSMS'], self.consumption['response']['consumption']['totalSMS']]
                self.voice = self.consumption['response']['consumption']['hybridVoice']
                self.data = [self.consumption['response']['consumption']['displayDataUsed'], str(round(float(self.consumption['response']['consumption']['totalData'])/1000)) + ' GB']
            else:
                self.days = 'Error!'
                self.sms = 'Error!'
                self.voice = 'Error!'
                self.data = 'Error!'
                self.report = 'Error!'
            self.report = tt.msg_maker(
                'Remaining days: ' + self.days,
                'Data: ' + self.data[0] + ' of ' + self.data[1],
                'Voice: ' + self.voice + ' min',
                'SMS: ' + self.sms[0] + ' of ' + self.sms[1]
            )
            if self.balance['success']:
                return True
            else:
                return False

        self.auth_session(get)

# e = entel()
# e.refresh()
# print(e.report)