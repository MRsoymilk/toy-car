import cv2
import sys
import os
import configparser
import numpy as np

Size = None

def image_threshold(target):
    image = cv2.imread(target, cv2.IMREAD_GRAYSCALE)
    image = image[0:160, 0:320]
    image = cv2.GaussianBlur(image, (5, 5), 0)
    clahe = cv2.createCLAHE(3, (3, 3))
    image = clahe.apply(image)
    _, image = cv2.threshold(image,  80, 255, cv2.THRESH_BINARY_INV)
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    image = cv2.resize(image, (32, 32))
    cv2.imwrite(target, image)

def operation(target):
    global Size
    image_threshold(target)

def file_walk(walk_path):
    for filepath, dirnames, filenames in os.walk(walk_path):
        for filename in filenames:
            target = os.path.join(filepath, filename)
            if os.path.getsize(target) == 0:
                print('\n', "delete file: ", target)
                os.remove(target)
            else:
                print('\r', "operate on ", target, end='', flush=True)
                operation(target)
    print('\n')

def main():
    if len(sys.argv) < 2:
        print("usage: ") 
        print("python reshape.py path")
    else:
        global Size
        config = configparser.ConfigParser()
        config.read('./config.ini')
        Size = config.getint('Picture', 'Size')
        print("reshape start ---- ", sys.argv[1])
        file_walk(sys.argv[1])
        print("reshape end   ---- ", sys.argv[1])

if __name__ == '__main__':
    main()

