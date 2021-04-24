import os
import configparser

config = configparser.SafeConfigParser()

config.read("conf.cfg")
#config.read("client/conf.cfg")

SERVER_IP = config.get('server-connection', 'IP')
SERVER_PORT = int(config.get('server-connection', 'PORT'))
DEBUG_MODE = "True" == config.get('debug', 'DEBUG_MODE')
CALL_NUMBER = int(config.get('debug', 'CALL_NUMBER'))
