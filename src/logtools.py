import datetime
import logging
 
def log_start(module_filename):
    today = datetime.datetime.now()
    filename = today.strftime("%y%m%d") + '_' + module_filename + '.log'
    logging.basicConfig(filename= filename, format='%(asctime)s - %(levelname)s / %(module)s / %(funcName)s / %(message)s', datefmt='%y/%m/%d - %H:%M:%S', level=logging.INFO)

    # logging.debug('This is a debug message')
    # logging.info('This is an info message')
    # logging.warning('This is a warning message')
    # logging.error('This is an error message')
    # logging.critical('This is a critical message')