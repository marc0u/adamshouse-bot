import logging

from src.generaltools import json_from_file

settings = json_from_file('settings.json')

settings['hello']
