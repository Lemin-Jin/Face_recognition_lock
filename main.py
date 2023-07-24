import cv2 
import os,glob
#import NumPy as np

counter = 0
# 0 is webcam, 1 is iphone cam, 2 is mac local cam
cap = cv2.VideoCapture(0) 
current_directory = os.getcwd()
os.chdir("/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/cv2/data")
# print(os.getcwd())
# files = glob.glob('*.jpeg')
# known_face_encodings = []
# known_face_names = []
# known_face = face_recognition.load_image_file("/Users/lejin/Documents/face_recognition_lock/faces/Lemin_Jin3.jpg")
# knonw_face_encoding = face_recognition.face_encodings(known_face)[0]
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

print(current_directory + "/faces")
while True:
    ret, frame = cap.read()

    cur_frame = frame.copy()

    face_rec = face_cascade.detectMultiScale(cur_frame, scaleFactor = 1.2, minNeighbors = 5, minSize = (120,120))
    
    for(x,y,w,h) in face_rec:
        cv2.rectangle(cur_frame, (x,y),(x+w,y+h), (255,0,0), 10)
    
    cv2.imshow("face detection", cur_frame)
    os.chdir(current_directory + "/faces")
    if counter <= 10 and len(face_rec) != 0:
        filename = "Lemin" + str(counter) + ".jpg"
        cv2.imwrite(filename, frame)
        print("saved")
        counter = counter + 1


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


# for file in files:
#     known_face = face_recognition.load_image_file(file)
#     knonw_face_encoding = face_recognition.face_encodings(known_face)
#     known_face_encodings.append(knonw_face_encoding)
#     known_face_names.append(str(file).replace(".jpg",""))
# print(known_face_encodings)
