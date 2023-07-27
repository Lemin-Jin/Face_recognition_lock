import cv2 
import os
import time

class profile:
    def __init__(self, name, num_pics, path, display, time_out):
        self.name = name
        self.num_pics = num_pics
        self.path = path
        self.display = display
        self.time_out = time_out
    def store_img(self):
        start = time.time()
        counter = 0
        # 0 is webcam, 1 is iphone cam, 2 is mac local cam
        cap = cv2.VideoCapture(0) 
        current_directory = self.path
        os.chdir("/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/cv2/data")

        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        while True:
            ret, frame = cap.read()

            cur_frame = frame.copy()

            face_rec = face_cascade.detectMultiScale(cur_frame, scaleFactor = 1.2, minNeighbors = 5, minSize = (120,120))
            
            if self.display is True:
                for(x,y,w,h) in face_rec:
                    cv2.rectangle(cur_frame, (x,y),(x+w,y+h), (255,0,0), 10)
                
                cv2.imshow("face detection", cur_frame)
            os.chdir(self.path)
            if counter <= self.num_pics and len(face_rec) != 0:
                filename = self.name + str(counter) + ".jpg"
                cv2.imwrite(filename, frame)
                counter = counter + 1
                
            if counter > self.num_pics:
                cap.release()
                cv2.destroyAllWindows()
                return True

            if time.time() - start > self.time_out:
                cap.release()
                cv2.destroyAllWindows()
                break
        return False
    
