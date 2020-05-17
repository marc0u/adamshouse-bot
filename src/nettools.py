import json
import logging
import requests
 
import src.generaltools as gt

class AuthSession:
    _AUTH_URL = None
    _AUTH_DATA = None
    _AUTH_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'}
    _cookies = None
    _retries = (3, 1)
    _timeout = (3, 3)

    @gt.with_retry(_retries)
    def perform_auth(self, allow_redirects=False) -> bool:
        if not(self._AUTH_URL) or not(self._AUTH_DATA):
            logging.error('_AUTH_URL and _AUTH_DATA properties are not found.')
            return False
        with requests.Session() as s:
            try:
                auth = s.post(self._AUTH_URL, data=self._AUTH_DATA, timeout=self._timeout, allow_redirects=allow_redirects)
                if (auth.status_code >= 400):
                    err = 'Http status code error: ' + str(auth.status_code)
                    logging.error(err)
                    self._cookies = None
                    return False
                if not s.cookies:
                    err = 'Cookie could not be got.'
                    logging.error(err)
                    self._cookies = None
                    return False
                ## Successful return
                self._cookies = s.cookies
                return True
            except requests.exceptions.ConnectTimeout:
                logging.error('Conection Timeout Error.')
                self._cookies = None
                return False
            except requests.exceptions.ConnectionError:
                logging.error('Conection Error.')
                self._cookies = None
                return False
            except requests.exceptions.ReadTimeout:
                logging.error('Read Timeout Error.')
                self._cookies = None
                return False
            except Exception:
                logging.exception("Exception occurred")
                self._cookies = None
                return False

    @gt.with_retry(_retries)
    def get(self, url, allow_redirects=True, timeout=_timeout):
        if not self.perform_auth():
            err = 'Could not got authentication from perform_auth() method.'
            logging.error(err)
            return None
        try:
            resp = requests.get(url, allow_redirects=allow_redirects, timeout=timeout, cookies=self._cookies)
            if resp.status_code >= 400:
                err = 'Http status code error: ' + str(resp.status_code)
                logging.error(err)
                return None
            ## Successful return
            return resp
        except requests.exceptions.ConnectTimeout:
            logging.error('Conection Timeout Error.')
            return None
        except requests.exceptions.ConnectionError:
            logging.error('Conection Error.')
            return None
        except requests.exceptions.ReadTimeout:
            logging.error('Read Timeout Error.')
            return None
        except Exception:
            logging.exception("Exception occurred")
            return None
    
    def get_content(self, url, allow_redirects=True, timeout=_timeout):
        resp = self.get(url, allow_redirects=allow_redirects, timeout=timeout)
        if resp == None:
            return None
        return resp.content.decode("utf8")
    
    def get_json(self, url, allow_redirects=True, timeout=_timeout) -> dict:
        resp = self.get_content(url, allow_redirects=allow_redirects, timeout=timeout)
        if resp == None:
            return None
        try:
            ## Successful return
            return json.loads(resp)
        except Exception:
            logging.exception("Exception occurred")
            return None

    @gt.with_retry(_retries)
    def post(self, url, data, allow_redirects=True, timeout=_timeout):
        if not self.perform_auth():
            err = 'Could not get authentication from perform_auth() method.'
            logging.error(err)
            return None
        try:
            resp = requests.post(url, data=data, timeout=timeout, allow_redirects=allow_redirects, cookies=self._cookies)
            if resp.status_code >= 400:
                err = 'Http status code error: ' + str(resp.status_code)
                logging.error(err)
                return None
            ## Successful return
            return resp
        except requests.exceptions.ConnectTimeout:
            logging.error('Conection Timeout Error.')
            return None
        except requests.exceptions.ConnectionError:
            logging.error('Conection Error.')
            return None
        except requests.exceptions.ReadTimeout:
            logging.error('Read Timeout Error.')
            return None
        except Exception:
            logging.exception("Exception occurred")
            return None

@gt.with_retry((3, 1))
def get_url(url, allow_redirects=True, timeout=(3, 5)):
    try:
        resp = requests.get(url, allow_redirects=allow_redirects, timeout=timeout)
        if (resp.status_code < 400):
            ## Successful return
            return resp
        if resp.status_code != 409:
            err = 'Http status code error: ' + str(resp.status_code)
            logging.error(err)
        return None
    except requests.exceptions.ConnectTimeout:
        logging.error('Conection Timeout Error.')
        return None
    except requests.exceptions.ConnectionError:
        logging.error('Conection Error.')
        return None
    except requests.exceptions.ReadTimeout:
        logging.error('Read Timeout Error.')
        return None
    except Exception:
        logging.exception("Exception occurred")
        return None

def get_content(url, allow_redirects=True, timeout=(3, 5)):
    resp = get_url(url, allow_redirects=allow_redirects, timeout=timeout)
    if resp == None:
        return None
    return resp.content.decode("utf8")

def get_json_from_url(url, allow_redirects=True, timeout=(3, 5)) -> dict:
    resp = get_content(url, allow_redirects=allow_redirects, timeout=timeout)
    if resp == None:
        return None
    try:
        ## Successful return
        return json.loads(resp)
    except Exception:
        logging.exception("Exception occurred")
        return None

def pretty_json(json_file) -> dict:
    try:
        return json.dumps(json_file, sort_keys=True, indent=4)
    except Exception:
            logging.exception("Exception occurred")
            return None