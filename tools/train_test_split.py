import os
import random
import configparser

def judge():
    rand_num = random.randint(1, 10)
    if rand_num <= 3:
        return "test"
    else:
        return "train"


def file_walk(walk_path, train, test, sub_path):
    for filepath, dirnames, filenames in os.walk(walk_path + sub_path):
        for filename in filenames:
            target = os.path.join(filepath, filename)
            if os.path.getsize(target) == 0:
                print('\n', "delete file: ", target)
                os.remove(target)
            else:
                print('\r', "operate on ", target, end='', flush=True)
                if judge() == 'test':
                    os.system("cp %s %s" % (target, test + sub_path))
                else:
                    os.system("cp %s %s" % (target, train + sub_path))
    print('\n')

def main():
    config = configparser.ConfigParser()
    config.read('./config.ini')
    File = config.get('Target', 'File')
    train = config.get('Network', 'Train')
    test = config.get('Network', 'Test')    
    print("train test split start ---- ")
    file_walk(File, train, test, 'a')
    file_walk(File, train, test, 'd')
    file_walk(File, train, test, 'w')
    print("train test split end   ---- ")

if __name__ == '__main__':
    main()
