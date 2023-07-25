import cv2
import os,glob
import face_recognition
import numpy as np
import time
import requests


cap = cv2.VideoCapture(0)
webhook_id = ""
url = ""
webhook_url = url + webhook_id
os.chdir(os.getcwd() + "/faces")
names = ["Lemin", "Charles"]

known_encodings = {}
[known_encodings.setdefault(name, []) for name in names]
for file_name in names:
    curfile = file_name + "?.jpg"
    files = glob.glob(curfile)
    print(files)
    for file in files:
        known_face = face_recognition.load_image_file(file)
        var =  face_recognition.face_encodings(known_face)
        if len(var) == 0:
            print(file)
        else:
            knonw_face_encoding = var[0]
            # print(len(known_encodings["Lemin"]))
            # print(len(known_encodings["Charles"]))
            known_encodings[file_name].append(knonw_face_encoding)
print("file encoding complete")
face_locations = []
face_encodings = []
face_names = []

verification_counter = {}
[verification_counter.setdefault(name, [0, time.time()]) for name in names]

to_process = True
while True:
    ret, frame = cap.read()
    if to_process == True:
        small_frame = cv2.resize(frame, (0,0), fx = 0.25, fy = 0.25)
        face_locations = face_recognition.face_locations(small_frame)
        
        # if len(face_locations) == 0:
        #     continue
        # print(len(face_locations))
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        face_names = []
        # loop through every face dectected in the frame
        for face_encoding in face_encodings:
            #loop through all the known names

            for key in known_encodings.keys():
                print(key)
                matches = face_recognition.compare_faces(known_encodings[key], face_encoding, tolerance= 0.4)
                print(matches)
                count = 0
                for item in matches:
                    if item == True:
                        count = count + 1
                if count/len(matches)  > 0.7:
                    face_names.append(key)
                    verification_counter[key][0] += 1

                
                if verification_counter[key][0] >= 5:
                    if time.time() - verification_counter[key][1] > 30: 
                        print("requst send")
                        r = requests.post(webhook_url)
                        verification_counter[key][1] = time.time()
                        verification_counter[key][0] = 0
            
        

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





