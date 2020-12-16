import configparser
import os

config = configparser.ConfigParser()
config.read('./config.ini')

if config.getboolean("View", "View"):
    os.system("python3 ./control/_View.py")
else:
    os.system("python3 ./control/_Cmd.py")
