import configparser
import os

config = configparser.ConfigParser()
config.read('./config.ini')

if config.getboolean("Network", "OpenVINO"):
    os.system("python3 ./network/_AutoAcc.py")
else:
    os.system("python3 ./network/_Auto.py")
