#computer vision library
import cv2

#This module helps to automate things on your pc. I'm using the press function to give the input to the computer
from pyautogui import press

#this module allows you to do multiprocessing, I'm using Queue to  communicate between processes
from multiprocessing import Process, Queue

#This is to tell the program what a face look like.
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#creating a video capture object and setting resolution.
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

#this is reference point and uing this point program knows in which direction face is moving 
refpoint=None

#it's a class to store point imformation
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


#It's the first process, and it shows the webcam view 
def show_webcam(arg):
    global refpoint
    q = arg
    while True:
        #getting frames and converting to grayscale image 
        success, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #Detects the faces in the frame
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        #looping over all the detected faces and drawing rectangles
        for (x, y, w, h) in faces:
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            #If the face is detected first time it sets its postion as a reference point
            if refpoint is None:
                refpoint = Point(x, y)

            else:
                #if latest detected face is right of the reference point (cam show mirror image so left is right)
                if x < refpoint.x - 30:
                    # print("right")
                    #sending input to the controller process 
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
        #showing each frame 
        cv2.imshow('video',img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break




#message queue to establish interprocess communication 
q = Queue(maxsize=1)

#Controller process which receives the input from show_webcam proces gives input to the computer
def controller(q):
    while True:
        key = q.get()
        print(key)
        press(key)

#Starting the actual processes
p1 = Process(target=show_webcam, args=(q,))
p1.start()
p2 = Process(target=controller, args=(q,))
p2.start()

