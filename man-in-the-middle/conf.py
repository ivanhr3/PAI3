import os
import configparser

config = configparser.SafeConfigParser()

config.read("conf.cfg")

SERVER_IP = config.get('server-connection', 'IP')
SERVER_PORT = int(config.get('server-connection', 'PORT'))
MITM_IP = config.get('mitm-connection', 'IP')
MITM_PORT = int(config.get('mitm-connection', 'PORT'))
DEBUG_MODE = "True" == config.get('debug', 'DEBUG_MODE')
NEW_ACCOUNT = config.get('attacks', "ACCOUNT_MODIFY")
REPLY_CHANCE = float(config.get('attacks', "REPLY_CHANCE"))
MODIFY_CHANCE = float(config.get('attacks', "MODIFY_CHANCE"))
