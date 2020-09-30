import threading
import time
import configparser
from gpiozero import Motor, Servo
from flask import Flask, render_template, Response

from GetChar import GetChar
from CarCamera import CarCamera


app = Flask(__name__)

print("load config")
config = configparser.ConfigParser()
config.read('./config.ini')

print("init car module")

carCamera = CarCamera()
getchar = GetChar()

motor = Motor(config.getint('Pin', 'MotorA'), config.getint('Pin', 'MotorB'))
Speed = config.getfloat('Car', 'Speed')
direction = Servo(config.getint('Pin', 'Direction'))
Left = config.getfloat('Car', 'Left')
Right = config.getfloat('Car', 'Right')

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(carCamera), mimetype='multipart/x-mixed-replace; boundary=frame')


KEEP_GOING = True

File = config.get('Target', 'File')

def keyboard_control():
    global KEEP_GOING
    global File
    global Speed, Left, Right
    while KEEP_GOING:
        cmd = getchar() 
        
        if cmd == 'q':
            KEEP_GOING = False
            motor.stop()
            direction.value = 0
            print("exit...")
            print("press Ctrl + c to exit web view")
        elif cmd == ' ':
            print("Car power on")
            motor.forward(Speed)
        elif cmd == 'w':
            print('forward')
            direction.value = 0
            threading.Thread(target=carCamera.capture, args=(File + 'w/' + str(time.time()) + '.png',)).start()
        elif cmd == 'a':
            print('left')
            direction.value = Left
            threading.Thread(target=carCamera.capture, args=(File + 'a/' + str(time.time()) + '.png',)).start()
        elif cmd == 'd':
            print('right')
            direction.value = Right
            threading.Thread(target=carCamera.capture, args=(File + 'd/' + str(time.time()) + '.png',)).start()
        else:
            print("cmd: ", cmd)
            motor.stop()


def main():
    threading.Thread(target=app.run, args=('0.0.0.0', 8080,)).start()
    threading.Thread(target=keyboard_control).start()

if __name__ == '__main__':
    main()  

