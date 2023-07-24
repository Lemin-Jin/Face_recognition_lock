import cv2
import os,glob
import face_recognition
import numpy as np
import time
import requests


cap = cv2.VideoCapture(0)
webhook_url = 'http://192.168.1.154:8123/api/webhook/-FMVJVIWEkBg4BOtauZMYOIjW'
os.chdir(os.getcwd() + "/faces")
files = glob.glob('Lemin?.jpg')
known_encodings = {"Lemin" :[]}
for file in files:
    known_face = face_recognition.load_image_file(file)
    knonw_face_encoding = face_recognition.face_encodings(known_face)[0]
    known_encodings["Lemin"].append(knonw_face_encoding)

face_locations = []
face_encodings = []
face_names = []
verification_counter = dict.fromkeys(['Lemin'], [0, time.time()])
to_process = True
while True:
    ret, frame = cap.read()

    if to_process == True:
        small_frame = cv2.resize(frame, (0,0), fx = 0.25, fy = 0.25)
        face_locations = face_recognition.face_locations(small_frame)

        if len(face_locations) == 0:
            continue
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        face_names = []
        # loop through every face dectected in the frame
        for face_encoding in face_encodings:
            #loop through all the known names
            for key in known_encodings.keys():
                matches = face_recognition.compare_faces(known_encodings[key], face_encoding)
                count = 0
                for item in matches:
                    if item == True:
                        count = count + 1
                if count/len(matches) > 0.6:
                    face_names.append(key)
                    verification_counter[key][0] += 1
                else:
                    face_names.append("unknown")
                count = 0

                if verification_counter[key][0] >= 5:
                    if time.time() - verification_counter[key][1] > 100: 
                        # send door signal
                        print("open door request sent")
                        r = requests.post(webhook_url)
                        print("cur_time diff = " + str (time.time() - verification_counter[key][1]))
                        verification_counter[key][1] = time.time()
                        print("updated diff = " + str (time.time() - verification_counter[key][1]))
                        verification_counter[key][0] = 0
                        # reset timer     
        

        for (top, right, bottom, left), name in zip(face_locations, face_names):

            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    to_process = not to_process

cap.release()
cv2.destroyAllWindows()





