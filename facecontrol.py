import cv2
from pyautogui import press
from multiprocessing import Process, Queue
import time
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

refpoint=None

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def show_webcam(arg):
    global refpoint
    q = arg
    while True:
        success, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            if refpoint is None:
                refpoint = Point(x, y)

            else:
                if x < refpoint.x - 30:
                    # print("right")
                    q.put("right")
                if x > refpoint.x + 30:
                    # print("left")
                    q.put('left')
                if y > refpoint.y + 20:
                    # print("down")
                    q.put('down')

                if y < refpoint.y - 5:
                    # print("up")
                    q.put('up')

        cv2.imshow('video',img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break





q = Queue(maxsize=1)


def consumer(q):
    while True:
        key = q.get()
        print(key)
        press(key)


t1 = Process(target=show_webcam, args=(q,))
t1.start()
t2 = Process(target=consumer, args=(q,))
t2.start()
t1.join()
t2.join()
