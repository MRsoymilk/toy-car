import os
import configparser


config = configparser.ConfigParser()
config.read('./config.ini')

Host = config.get('Target', 'Host')
File = config.get('Target', 'File')


try:
    print("Tar ", File)
    os.system("tar cvf images.tar -C %s ." %(File))
    print("Scp to ", Host)
    os.system("scp images.tar %s:/tmp" % (Host))
    print("Clean")
    os.system("rm images.tar")
    print("Finish")
except:
    print("it works on Linux, other platform may wrong in some commands")
